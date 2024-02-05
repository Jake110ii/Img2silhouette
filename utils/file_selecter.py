from PyQt5.QtWidgets import QApplication, QFileDialog

def open_file_dialog():
    app = QApplication([])

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getOpenFileName(None, "ファイルを選択", "", "すべてのファイル (*);;テキストファイル (*.txt)", options=options)
    
    return file_path


def main():
    open_file_dialog()


if __name__ == "__main__":
    main()
