# Dcentralab Assignment

## Project Description

This project includes an efficient web scraper and a RAG (Retrieval-Augmented Generation) search system that supports both semantic and keyword-based searches.

### Components:
1. **Web Scraper**:  
   - Scrapes the website `https://cryptorank.io/all-coins-list` to extract URLs for individual cryptocurrency coins.
   - Subsequently, scrapes each coin's page for specific data, such as the website, social media links, and other metadata, to generate a comprehensive description.
   - The extracted data is saved in:
     - `full_scrape.txt`: Contains detailed JSON data for the first 10 coins.
     - `data_dir/description.txt`: Stores token descriptions only.
   - Note: The scraping is limited to 10 coins to minimize API call costs.

2. **RAG Search System**:  
   - Enables robust search functionality that supports both semantic and keyword-based queries.
   - Provides answers to qualitative and quantitative questions about cryptocurrencies, based on the descriptions found in the `data_dir/description.txt` database.

---

## Libraries Used
- **Llama-index**
- **OpenAI**
- **Crawl4AI**
- **Flask**

---

## Running the Project

### 1. Create a Codespace and Build the Development Container
- Use GitHub Codespaces to create a development environment.
- When prompted, ensure you build the development container for proper functionality.

### 2. Install Dependencies and Activate the Virtual Environment
- Use the provided `Makefile` for easy setup. Run the following command in the terminal:
  ```bash
  make all

3. **Create a `.env` file**: 
   - Use the `.env_example` file as a reference.
   - This file should include your OpenAI API key.
   - Note: This step is necessary if you plan to run `scrapper.py` and `rag.py` from the terminal. 
   - Alternatively, you can view the scraped content in `full_scrape.txt` and token descriptions in `data_dir/description.txt`. The scraping process is limited to 10 coins to manage API costs.

4. **Run the Scraper and RAG Search System**:
   - To scrape data, execute:
     ```bash
     python scrapper.py
     ```
   - To run the RAG system, execute:
     ```bash
     python rag.py
     ```

5. **Run the Flask Application**:
   - You can skip running `scrapper.py` and `rag.py` directly.
   - Instead, start the Flask app by running:
     ```bash
     python app.py
     ```
   - Running the Flask app provides a URL where you can test the RAG search system through a simple HTML, CSS, and JavaScript interface.

6. **Note**:
   - The project is not deployed online; it is designed to be run locally.
   - The scraping process is limited to 10 coins to efficiently manage API costs.
