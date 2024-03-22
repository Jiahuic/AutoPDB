# AutoPDB
An AI-powered, simple, easy-to-use tool to automatically get the information from the RCSB PDB database.

## Features
There are a lot of protein complexes on the PDB database, which provides rich information. 
However, it is not easy to get the information of the protein complexes, such as the chains belonging to which part of the complex. 
This project is to provide a tool to automatically get the information of the protein complexes on the PDB database by using the PDB API and LLM.

## Installations
AutoPDB is written in Python and rely on `LangChain`. Simple to install and easy to use.

- [request](https://pypi.org/project/requests/) a third-party library for making HTTP requests in Python. The RCSB PDB API uses the GraphQL query language to access the data.
- [LangChain](https://www.langchain.com/) is a framework for developing applications powered by language models. 
- [OpenAI](https://www.openai.com/) provides the LLM model API. If you want to use the openai model, you need to sign up for an API key.
- [Ollama](https://ollama.com/) provides the open-source LLM model, which can run on your local machine. Open-source models such as llama2, mistral, and gemma are available. 

Install the required packages using the following command:
```bash
pip install requests
pip install langchain, langchain_openai, langchain_community
```

If you want to use the openai model, you need to sign up for an API key. 
```bash
echo "export OPENAI_API_KEY=your-api-key" >> ~/.bashrc # or ~/.zshrc
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
