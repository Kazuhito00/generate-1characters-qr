# generate-1characters-qr
QRコード保持情報とは別に、文字(アルファベット・数字・記号)を描画したQRコードを生成するプログラムです。<br>
管理タグ等にご使用ください。<br>
<img src="https://user-images.githubusercontent.com/37477845/122433251-02fa3a80-cfd1-11eb-9c6c-a85354465338.png" width="40%"> <img src="https://user-images.githubusercontent.com/37477845/122433246-01c90d80-cfd1-11eb-9e83-cb416a690b66.png" width="40%"> 

# Requirements
* Pillow 8.2.0 or Later
* amzqr 0.0.1 or Later

# Usage
実行方法は以下です。<br>
```bash
python generate_1characters_qr.py -w=sample -c=A
```
<br>
実行時には、以下のオプションが指定可能です。

* -w, --words<br>
QRコードに保持する文字列<br>
デフォルト：指定なし
* -c, --character<br>
QRコード上の描画する文字(1文字)<br>
デフォルト：指定なし
* -cc, --character_color<br>
QRコード上の描画する文字の文字色<br>r,g,b,y,m,c,p の何れかを指定可能<br>r : red、g : green、b : blue、y : yellow、m : magenta、c : cyan、p : purple<br>
デフォルト：指定なし
* -v, --version<br>
QRコードの最低バージョン<br>指定バージョンのコードで情報が保持しきれない場合は、保持可能な上位のバージョンでQRコードが作成されます<br>
デフォルト：1
* -l, --level<br>
エラー訂正レベル(L,M,Q,H)<br>
デフォルト：H
* -n, --save_name<br>
保存ファイル名<br>
デフォルト：qr.png
* -d, --save_dir<br>
保存ディレクトリ名<br>
デフォルト：指定なし(カレントディレクトリ)
* -f, --font<br>
フォント指定 ※フォントによってはQRコードからはみ出る可能性があります<br>
デフォルト：'font/umefont_670/ume-ugo5.ttf'

# Reference
* [x-hw/amazing-qr](https://github.com/x-hw/amazing-qr)

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
generate-1characters-qr is under [GPL-3.0 License](LICENSE).
