# 💣 炸彈人
爆炸吧！訓練你的 AI 來控制角色的移動，放置與躲避炸彈，成為最會炸的炸彈人吧！

## 玩法介紹
玩家需要在特定的時間內使用炸彈攻擊敵對玩家，獲得境可能多的分數。炸彈不會影響友方團隊的其他玩家，且當多個炸彈在彼此的爆炸範圍內就會產生 `連鎖爆炸`。另外地圖上的 `瓦磚 (Tile)` 會阻擋玩家的移動，玩家可以破壞地圖上 `可破壞的瓦磚 (Tile)` 來讓自己更好移動。

> 手動操作：
> * `w` `s` `a` `d` 移動角色。 
> * `z` 放置炸彈。

## 計分機制
* `炸到敵對玩家` + 2
* `被炸到` - 1

# 遊戲設定
你可以簡單的設置遊戲的參數，另外我們也提供了一個人類可讀的關卡檔案格式 (與編輯器)，讓你可以輕鬆的打照你心中的完美關卡！

## 遊戲參數
```py
Game(level_name: str, level_file: Union[None, str], width: int = 750, height: int = 500, user_num: int = 1, game_duration: int = 1800, team_mode: str = "off")
```
* `level_name: str` 關卡名稱 (遊戲預設的關卡名稱)。
* `level_file: str` 關卡檔案路徑，設置此參數會覆蓋掉 "level_name"。
* `width: int` 視窗的寬度。 
* `height: int` 視窗的高度。
* `user_num: int` 玩家的數量。
  * 範圍為 1 ~ 關卡支援的最大玩家數 (最大為 4)。
* `game_duration: int` 遊戲的時長 (幀數)。
* `team_mode: bool` 團隊模式。
  * 只在玩家數量為 2 個以上時才有用，在 3 個玩家時會有一對只有一個玩家。

## 關卡參數
我們有自己的關卡檔案格式 (.bomb)，以下為一個簡單的範例：
```
[Rules]
| player_speed: number(5)
| player_bombs: number(2)
|
| bomb_countdown: number(150)
| bomb_explode_range: number(125)

[Map]
| width: number(10)
| height: number(5)
|
| tiles_type: string_list(string(barrel))
| tiles_position: vec2_list(vec2(1:1))
|
| player_spawns: vec2_list(vec2(0:0), vec2(0:1), vec2(0:2), vec2(0:3))
```
* `Rules` 關卡規則。
  * `player_speed: number` 玩家的移動速度。
  * `player_bombs: number` 玩家的炸彈數。
  * `bomb_countdown: number` 炸彈的爆炸倒數計時時間 (幀數)。
  * `bomb_explode_range: number` 炸彈的爆炸範圍。
* `Map` 關卡的地圖
  * `width: number` 關卡的寬度 (幾個瓦磚)。
  * `height: number` 關卡的高度 (幾個瓦磚)。
  * `tiles_type: string_list` | 地圖上每個瓦磚的名稱，對照到 "tiles_position"。
  * `tiles_position: vec2_list` | 地圖上每個瓦磚的位置，對照到 "tiles_type"。
  * `player_spawns: vec2_list` | 玩家的重生點，清單的長度決定了最大的玩家數量。
