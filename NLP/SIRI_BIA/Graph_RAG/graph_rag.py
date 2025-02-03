import os
import sys

# Check for necessary libraries and install them if missing
def install_dependencies():
    try:
        import llama_index
        import neo4j
    except ImportError:
        if os.path.exists("SIRI_BIA\Graph_RAG\requirements.txt"):
            os.system("pip install -r requirements.txt")
        else:
            raise FileNotFoundError("requirements.txt not found. Please ensure it exists in the project directory.")

# Class to manage the Knowledge Graph interactions with Neo4j
class KnowledgeGraphManager:
    def __init__(self, uri, user, password):
        from neo4j import GraphDatabase

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

# Utility class to handle file reading using Llama Index
class FileReaderUtility:
    def __init__(self, data_dir):
        from llama_index.readers import file
        self.file_readers = {reader: getattr(file, reader) for reader in dir(file) if 'Reader' in reader}
        self.data_dir = data_dir

    def list_available_readers(self):
        return list(self.file_readers.keys())

    def read_file(self, reader_type, file_name):
        file_path = os.path.join(self.data_dir, file_name)
        if reader_type in self.file_readers:
            reader_class = self.file_readers[reader_type]
            return reader_class().load(file_path)
        else:
            raise ValueError(f"Unsupported reader type: {reader_type}")

# Main logic to initialize and execute the workflow
def main():
    install_dependencies()

    # Initialize KnowledgeGraphManager (replace with your credentials and URI)
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "your_password"
    graph_manager = KnowledgeGraphManager(uri, user, password)

    # Example Query
    query = "MATCH (n) RETURN n LIMIT 10"
    try:
        results = graph_manager.run_query(query)
        print("Query Results:", results)
    finally:
        graph_manager.close()

    # FileReader Example
    data_dir = "Dados"  # Path to the directory containing the data files
    file_reader = FileReaderUtility(data_dir)
    print("Available Readers:", file_reader.list_available_readers())

    # Example: Reading a Markdown file (replace 'sample.md' with an actual file name from 'Dados')
    try:
        reader_type = 'MarkdownReader'
        file_name = 'sample.md'
        content = file_reader.read_file(reader_type, file_name)
        print("File Content:", content)
    except Exception as e:
        print("File Reading Error:", e)

if __name__ == "__main__":
    main()
