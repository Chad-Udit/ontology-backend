# from neo4j import GraphDatabase


# def run_cypher_query(uri, user, password, query):
#     with GraphDatabase.driver(uri, auth=(user, password)) as driver:
#         with driver.session() as session:
#             result = session.run(query)
#             return result.data()

# def format_results(results):
#     formatted_results = []
#     for result in results:
#         # Extract relevant data from the result
#         node_data = result['p'].end.nodes[0]
#         name = node_data['first_name']
#         latitude = node_data['latitude']
#         longitude = node_data['longitude']
#         address = node_data['address']
        
#         # Create a dictionary with the extracted data
#         formatted_result = {
#             "name": name,
#             "latitude": latitude,
#             "longitude": longitude,
#             "address": address
#         }
        
#         # Append the formatted result to the list
#         formatted_results.append(formatted_result)
    
#     return formatted_results



# uri = "bolt://3.254.201.67:7687"  # Change the URI according to your Neo4j setup
# user = "neo4j"  # Change the username
# password = "password"  # Change the password
# # Define your Cypher query
# cypher_query = "MATCH p=()-[r:NEARBY]->() RETURN p LIMIT 25"
# # Execute the Cypher query
# results = run_cypher_query(uri, user, password, cypher_query)

# # Format the results
# formatted_results = format_results(results)

# # Print the formatted results (or do further processing)
# for result in formatted_results:
#     print(result)


