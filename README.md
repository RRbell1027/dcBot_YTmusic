# dcBot_YTmusic
對 YouTude 影片進行爬蟲，進而在 discord 撥放的機器人。<br>
純粹是自己用，有許多個人化的功能，如果要更改請自行做 code review。 <br>
雖然是依照多伺服器服務寫的，但沒測試過同時服務於多個 discord 伺服器的性能。<br>
以下依照:<br>
* Python 環境
* 程式碼使用
* 指令

做分類。

# Python 環境
* discord-py 1.7.3
* yt-dlp 2023.3.4

# 程式碼使用
請在程式碼所在資料夾中新建 buffers 資料夾，這個資料夾將會存放從 YouTube 下載的音樂。

當然，如果您有自己預設的資料夾，請更改 audio.py 中的 save_path 位置。

接著將 version1.py 中的 token 改為您的機器人 token 即可執行。

# 指令
所有指令皆以 '.' 開頭。
* play <url>：將音樂放入機器人撥放清單當中，等待撥放。(注意：url 請輸入 YouTube 影片網址，不要包含撥放清單，也不能是會員限制或私人影片)
* pause：暫停撥放
* resume: 繼續撥放
* skip: 結束撥放目前音樂

注意：當機器人撥放清單中只有單一歌曲時，將會循環撥放該歌曲。
