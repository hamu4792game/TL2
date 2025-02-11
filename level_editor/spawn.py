import bpy.ops
import os

class SpawnNames():

    # インデックス
    PROTOTYPE = 0  #プロトタイプのオブジェクト名
    INSTANCE = 1   #量産時のオブジェクト名
    FILENAME = 2   #リソースファイル名

    names = {}
    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["Enemy"] = ("PrototypeEnemySpawn", "EnemySpawn", "enemy/enemy.obj")
    names["Player"] = ("PrototypePlayerSpawn", "PlayerSpawn", "player/player.obj")

class MYADDON_OT_spawn_load_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_load_symbol"
    bl_label = "出現ポイントシンボルを読み込む"
    bl_description = "出現ポイントのシンボルを読み込みます"

    def load_obj(self, type):
        print("出現ポイントのシンボルを読み込みます")

        spawn_object = bpy.data.objects.get(SpawnNames.names[type][SpawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {"CANCELLED"}

        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory = os.path.dirname(__file__)
        # 合成してモデルファイルのフルパスを得る
        full_path = os.path.join(addon_directory, SpawnNames.names[type][SpawnNames.FILENAME])

        # オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',
                            filepath = full_path, display_type = 'THUMBNAIL',
                            forward_axis = 'Z', up_axis = 'Y')
        
        # 回転を適用
        bpy.ops.object.transform_apply(location = False,
                                    rotation = True, scale = False, properties = False,
                                    isolate_users = False)
        
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name = SpawnNames.names[type][SpawnNames.PROTOTYPE]
        # オブジェクトの種類を設定
        object["type"] = SpawnNames.names[type][SpawnNames.INSTANCE]

        # メモリ上にはおいておくがシーンから外す
        bpy.context.collection.objects.unlink(object)

        return {"FINISHED"}
    
    def execute(self, context):
        # Enemyオブジェクト読み込み
        self.load_obj("Enemy")
        # Playerオブジェクト読み込み
        self.load_obj("Player")

        return {"FINISHED"}
    

class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボル作成"
    bl_description = "出現ポイントシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    # プロパティ
    type: bpy.props.StringProperty(name = "Type", default = "Player")

    def execute(self, context):
        # 読み込み済みのコピー元オブジェクトを検索
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        # まだ読み込んでいない場合
        if spawn_object is None:
            # 読み込みオペレータを実行する
            bpy.ops.myaddon.myaddon_ot_spawn_load_symbol('EXEC_DEFAULT')
            # 再建策
            spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        print("出現ポイントのシンボルを作成します")

        # Blenderでの選択を解除する
        bpy.ops.object.select_all(action = 'DESELECT')

        # 複製元の非表示オブジェクトを複製する
        object = spawn_object.copy()

        # 複製したオブジェクトを現在のシーンにリンク（出現させる）
        bpy.context.collection.objects.link(object)

        # オブジェクト名を変更
        object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        return {"FINISHED"}
    

class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT', type = "Player")

        return {"FINISHED"}


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT', type = "Enemy")

        return {"FINISHED"}