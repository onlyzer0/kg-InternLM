from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph
class Neo4jQueryHandler:
    def __init__(self, uri, user, password):
        self.kg = Neo4jGraph(url=uri, username=user, password=password, database='neo4j')

    @staticmethod
    def build_query(category, text):
        # 这里根据不同的类别构建不同的Cypher查询语句
        # 仅作为示例，实际情况需要根据你的数据模型调整
        if category == "1":
            island=text
            return f"MATCH (p:`作者`)<-[r]-(:`论文`)-[r2]->(a:`海岛`{{`名称`:'{island}'}}) return p.`姓名`"
        elif category == "2":
            island = text
            return f"MATCH (a:`海岛`{{`名称`:'{island}'}}) RETURN a.`名称`, a.`东经`,a.`北纬`"
        else:
            raise ValueError("抱歉，暂未提供此类型查询功能！")

    def query_and_return(self,category, text):
        if category=='1':
            answer = '相关研究人员名单：'
        elif category=='2':
            answer=f'{text}位置:'
        else:
            answer=''
        query = self.build_query(category, text)
        results = self.kg.query(query)
        formatted_strings = ['({}, {})'.format(list(item.keys())[0], list(item.values())[0]) for item in results]
        answers =answer+ ';'.join(formatted_strings)
        return answers
# 使用示例
if __name__ == "__main__":
    neo4j_handler = Neo4jQueryHandler("bolt://localhost:7687", "neo4j", "neo4j1234")

    # 假设我们要查询类别为"person"，名字为"John Doe"的记录
    results = neo4j_handler.query_and_return("1", "东海岛")
    print(results)


