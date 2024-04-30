from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
graph = Neo4jGraph(
    url="bolt://54.172.172.36:7687",
    username="neo4j",
    password="steel-foreheads-examples")
chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), 
    graph=graph, verbo

graph_result = chain.run("Who were the siblings of Leonhard Euler?")se=True,)