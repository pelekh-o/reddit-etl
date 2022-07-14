# reddit-etl

## Project workflow
0. **Setup Airflow on Docker (details [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html))**

    * Download ```docker-compose.yaml``` 
        ```bash
        curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.2/docker-compose.yaml'
        ```
    * Add volume to save the extracted files
        ```yaml
        - ./files:/opt/airflow/files
        ```
    * Add required libraries to the ```docker-compose.yaml``` 
        ```yaml
        _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- praw pandas pygsheet}
        ```
         This is a development/test feature only. NEVER use it in production!
Instead, build a custom image as described in [the docs](https://airflow.apache.org/docs/docker-stack/build.html) .
    * In the project/airflow directory run 
        ```bash
        mkdir -p ./dags ./logs ./plugins
        ```
    * Run the next command to create ```.env``` file next to ```docker-compose.yaml```:
        ```yaml
        echo -e "AIRFLOW_UID=$(id -u)" > .env
        ```
    * Initialize the database to run database migrations and create the first user account
        ```bash
        docker-compose up airflow-init
        ```
        The account created has the login airflow and the password airflow
    
    * Now run the Airflow
        ```bash
        docker-compose up
        ```
        The Airflow webserver is available at http://localhost:8080


1. **Setup Reddit App**
    * First, you'll need an active reddit account
    * Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps). If previous link doesn't work for you, try [old.reddit.com/prefs/apps/](https://old.reddit.com/prefs/apps/)
    * Select **create another app**. Make sure to select **Script** option
    * Fill in description and optional fields. Click **create app**
    * Next you will see your client id and secret. These values will be 
    needed in the next steps


2. *[Optional]* **Create a Virtual Environment Install Airflow**
    * Create a Virtual Environment
        ```bash
        python3 -m venv venv
        ```
    * Activate 
        ```bash
        source venv/bin/activate
        ```
    * Install Airflow libs
        ```bash
        pip install apache-airflow
        ```

3. **Add the dag files**
    * Create ```pipeline.conf``` file inside ```dags/extraction``` directory with your reddit app credentials
        ```conf
        [reddit]
        client_id = your_script_client_id
        client_secret = your_script_client_secret
        ```