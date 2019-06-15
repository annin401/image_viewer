'''
イメージを表示する画面
MainWindowの代わり
'''
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from ImagePaths import ImagePaths
from ImageViewScene import ImageViewScene

class ImageViewer( QtWidgets.QGraphicsView ):
        def __init__(self):
                super().__init__()

                self.image_paths =  ImagePaths()
                self.window_height = 400.0
                self.window_width = 600.0
                self.current_pos = QtCore.QPoint(400, 400) # 初期座標は(400, 400)

                self.set_imageViewer()
                self.init_menu()

                # for slideshow
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.update) 
                self.update_interval = 2000 # ミリ秒

                # for self.update
                self.path_index = 0

                # for move window
                self.clicked_pos = QtCore.QPoint()

        def set_imageViewer(self):
                # フラグセット
                self.setWindowFlags(QtCore.Qt.CustomizeWindowHint) # タイトルバーを消す
                self.setFixedSize(self.window_width, self.window_height) # サイズを固定
                self.move(self.current_pos) # ウィンドの場所を移動
                # TODO 初期位置右下にする

                # QGraphicsViewの設定
                self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)        
                self.setRenderHints(QtGui.QPainter.Antialiasing |
                        QtGui.QPainter.SmoothPixmapTransform |
                        QtGui.QPainter.TextAntialiasing
                )

                # QGraphicsSceneの作成・および設定.
                scene = ImageViewScene(self.window_width, self.window_height)
                scene.setSceneRect( QtCore.QRectF( self.rect()))
                self.setScene(scene)
            
        def init_menu(self):
            pass # TODO メニューを作る


        def show_set_Dialog(self):

            # ファイルダイアログを表示
            dirpath = QtWidgets.QFileDialog.getExistingDirectory(self,
                'Select Folder', os.path.expanduser('~'),
                )

            # フォルダーが選択されなかったら終了
            if dirpath == '':
                return 

            # 画像パスのリストを生成
            self.image_paths.make_list(dirpath)

        def start_slideshow(self):

            if not self.image_paths:
                return 

            # 画像更新をする関数を呼び出すタイマーをスタートする
            self.timer.start(self.update_interval)

            # 最初に表示する画像をセットする
            self.update()


        def update(self):

            # インデックスが最後まで到達したら最初に戻す
            if self.path_index == len(self.image_paths):
                self.path_index = 0

            # 画像をセットする
            self.scene().set_file( self.image_paths[self.path_index] )

            # インデックスを更新
            self.path_index += 1 

        def resizeEvent(self, event):
             # ビューをリサイズ時にシーンの矩形を更新する
             super().resizeEvent( event )   
             self.scene().setSceneRect(QtCore.QRectF(self.rect()))

        def mousePressEvent(self, e):
             # 左クリック時にウィンドを移動させる準備
             if e.button() == QtCore.Qt.LeftButton:
                 self.clicked_pos = e.pos() # ウィンドの左上を(0,0)にした相対位置

        def mouseMoveEvent(self, e):
             # 左クリック時にドラッグでウィンドを移動
            if e.button() == QtCore.Qt.LeftButton:
                # マウスの移動距離を求める
                distance = e.pos() - self.clicked_pos
                # 現在位置を更新
                self.current_pos += distance 
                self.move(self.current_pos)



# for debug
app = QtWidgets.QApplication([])
v = ImageViewer()
v.show()
v.show_set_Dialog()
v.start_slideshow()
import sys
sys.exit(app.exec_())
