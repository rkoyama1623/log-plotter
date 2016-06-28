# plotterのメモ

## 各viewにアクセス
```
a.plotItemOrig2
v.items
item=v.items[0]
item.getData()
````

## getattrで呼び出される関数の引数
args, indices_list, arg_indices, cur_col, key, i
['RobotHardware0_rfsensor'] [[0]] [0] 0 RobotHardware0_rfsensor 1

args:関数の引数として渡されるlogファイル名
indices:arg_indicesの中のどの情報を利用するか
arg_indices:各ファイルの何列目を使用するか
cur_col:現在描画中の列数(行数は不明)
key:判例に表示する名前
i:一つのグラフの中の何番目の判例を書いているか

plot_xxxで記述しているのは、`cur_col`が与えられた時、
`data_dict[args[0]]`(=ex. `st_q`)
の何列目を描画するのかということで、
今まで、indexを直接与えていたが、それを、`indices_list[arg_indices[0]][cur_col]`で指定する。
```
index->indices_list[arg_indices[0]][cur_col]
```


`indices_list[log_file_name][cur_col]`で、`cur_col`に対して、`log_file_name`の何列目を参照するべきかがわかる。



```
@staticmethod
def normal(plot_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i):
plot_item.plot(times, data_dict[args[0]][:, indices_list[arg_indices[0]][cur_col]], pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=2), name=key)
```

