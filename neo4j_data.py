# from neo4j import GraphDatabase

# uri = "bolt://3.254.201.67:7687"  # Change the URI according to your Neo4j setup
# user = "neo4j"  # Change the username
# password = "password"  # Change the password

# # Create a Neo4j driver instance
# driver = GraphDatabase.driver(uri, auth=(user, password))

# # Define your Cypher query
# cypher_query = "MATCH p=()-[r:NEARBY]->() RETURN p LIMIT 25"

# # Run the query within a session
# with driver.session() as session:
#     result = session.run(cypher_query)
#     for record in result:
#         print(record)

# driver.close()
