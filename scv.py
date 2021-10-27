# coding: UTF-8
import glob 
import json
import re
from graphviz import Graph

# 社員リスト作成
employee_list = {}
json_files = glob.glob("./20211026_slack/*/*.json")
for file in json_files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)
    for v in json_load:
        if 'user_profile' in v : # 写真の投稿のみの場合'user_profile'が存在しないためエラーを回避する
            employee_list[v['user']] = v['user_profile']['real_name']

# コミュニケーションの解析
employee_commication_list = {}
pattern = '<@(.*?)>' # メンションのパターン

# 特定のプロジェクトを確認する時はここを変更する
json_files = glob.glob("./20211026_slack/pj-coda/*.json")

for file in json_files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)
    for v in json_load:
        if 'user' in v and 'text' in v and re.findall(pattern,v['text']):
            employee_commication_list[v['user']] = []
            partners = re.findall(pattern,v['text'])
            for partner in partners:
                #線の重複を防ぐため、自分のキーに相手がいない かつ 相手のキーがあり相手のキーに自分がいない場合のみコミュニケーション先を追加
                if not partner in employee_commication_list[v['user']] and not (partner in employee_commication_list and v['user'] in employee_commication_list[partner]):
                    employee_commication_list[v['user']].append(partner)

# dot作成（集計）
graph = Graph(format='svg', engine='fdp')

for employee in employee_commication_list:
    if employee in employee_list:  
        for you in employee_commication_list[employee]:
            i = employee_list[employee]
            if you in employee_list:
                u = employee_list[you]
                graph.edge(i,u) # 辺を追加

# 画像を保存
graph.render("image/pj-coda")

# 画像を表示
graph.view()