kai_kun3
===

* つれづれなるままに動く家庭タスクのbotの情報一覧
* 動作場所は、`ich1family.slack.com`

# 仕事一覧

## チャンネル: `#shoppinglist`

| 命令文(ja) | 命令文(en) | 簡単な説明 |
| :---:  | :---: | :---: |
| `<食材名>` | - | <食材名> をお買い物リストに追加します。 `@kai add` のaliasです。|
| `@kai 一覧 [全部\|済]` | `@kai list [all\|closed]` | 現在のお買い物リストを表示します|
| `@kai 削除 <食材名>` | `@kai del <食材名>` | <食材名> を削除します(お買い物リストで表示できなくします) |
| `@kai 追加 <食材名>` | `@kai add <食材名>` | <食材名> をお買い物リストに追加します |
| `@kai 済 <食材名>` | `@kai close <食材名>` | <食材名> が既にある場合は、買い物済みにします |

## チャンネル: `#command`

# maintenance

## 注意事項
proxyの指定は、`export http_proxy=http://proxy.example.com:8080/`じゃなくて、`export http_proxy=proxy.exmaple.com:8080`

## 内容

* [setup](ope/setup.md)
