# coding: UTF-8
import glob 
import json
import re
from graphviz import Graph

# 社員リスト作成
employee_list = {}
json_files = glob.glob("./logs/*/*.json")
for file in json_files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)
    for v in json_load:
        if 'user_profile' in v : # 写真の投稿のみの場合'user_profile'が存在しないためエラーを回避する
            employee_list[v['user']] = v['user_profile']['real_name']

# コミュニケーションの解析
commication = []
json_files = glob.glob("./logs/*/*.json") # 特定のチャンネルを確認する時はここを変更する
pattern = '<@(.*?)>' # メンションのパターン
graph = Graph(format='svg', engine='sfdp')
path = []
before_path = []

for file in json_files:
    before_path = path 
    path =  re.findall('./logs/(.*)/', file)
    json_open = open(file, 'r')
    json_load = json.load(json_open)
    
    # 同じチャンネルの間であればノードを追加する
    if not before_path or path == before_path:
        for v in json_load:
            if 'user' in v and re.findall(pattern,v['text']):            
                partners = re.findall(pattern,v['text']) # メンション先（複数）
                for partner in partners:
                    #線の重複防止処理
                    if not partner+v['user'] in commication:
                        # メンション先でチャンネルに参加してないユーザのIDを名前として登録
                        if not partner in employee_list:
                            employee_list[partner] = partner
                        if not v['user'] in employee_list:
                            employee_list[v['user']] = v['user']
                        # ノード+線を追加            
                        graph.edge(employee_list[partner],employee_list[v['user']])
                        # 重複チェック用配列に追加
                        commication.append(v['user']+partner) 
                        commication.append(partner+v['user']) 
    else:
        # 画像を保存
        graph.render("image/" + before_path[0])
        #チャンネルごとにリセット
        graph.clear()
        commication = []

# 画像を表示
graph.render("image/" + path[0])
# graph.view() # 画像を見たい時用