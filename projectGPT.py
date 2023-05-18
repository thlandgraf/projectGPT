import argparse
import os
import datetime
import time
import threading
import quart
import quart_cors
from quart import abort, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WORKDIR = "/Users/tl/hack/projectGPT"

args = None

# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.post("/query")
async def query():
    host = request.headers['Host']
    rq = await quart.request.get_json(force=True)
    try:
        results = []
        for query in rq["queries"]:
            searchresults = best_matches(query["query"])
            result = {
                "query": query["query"],
                "results": [
                    {
                        "text": searchresult["text"],
                        "metadata": {
                            "source": "file",
                            "source_id": os.path.basename(searchresult['filepath']),
                            "url": f"http://{host}/file{searchresult['filepath'].replace(args.docpath,'',1)}",
                            "created_at": None,
                            "author": None
                        },
                        "score": searchresult["score"]
                    } for searchresult in searchresults if searchresult["score"] > 0]
            }
            results.append(result)
        return results
    except Exception as e:
        print("Error:", e)
        abort(500)

@app.get("/file")
@app.get("/file/<string:path_or_name>")
async def get_file(path_or_name):
    global files, args
    host = request.headers['Host']
    result = []
    for file in files:
        if path_or_name in file['filepath']:
            result.append({
                "text": file['text'],
                "metadata": {
                    "source": "file",
                    "source_id": os.path.basename(file['filepath']),
                    "url": f"http://{host}/file{file['filepath'].replace(args.docpath,'',1)}",
                    "created_at": None,
                    "author": None,
                    "document_id": "4a3d5980-8dbc-433e-86ca-52811b5e0743"
                },
            })
    if len(result) == 0:
        return "Nothing found, please use /query to search"
    return { "query": path_or_name, "results": result }

@app.get("/logo.png")
async def plugin_logo():
    filename = f'{WORKDIR}/.well-known/logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open(f'{WORKDIR}/.well-known//ai-plugin.json') as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"http://{host}")
        text = text.replace("PROJECTNAME", args.name)
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open(f"{WORKDIR}/.well-known/openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"http://{host}")
        text = text.replace("PROJECTNAME", args.name)
        return quart.Response(text, mimetype="text/yaml")
    
def load_file_data(filepath):
    with open(filepath, 'r') as f:
        text = f.read()
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    return {'filepath': filepath, 'last_modified': last_modified, 'text': text}
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def best_matches(search_string, top_n=3):
    global files
    # Extract the texts from the data
    texts = [entry['text'] for entry in files]
    
    # Add the search string to the list of texts
    texts.append(search_string)

    # Transform texts into TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(texts)

    # Compute cosine similarities between the search string and all texts
    # The search string is the last element (-1), so we get its similarities with all others
    cosine_similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

    # Get the indices of the top_n most similar texts
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]

    # Build the result array with the required fields
    result = []
    for i in top_indices:
        result.append({
            "text": files[i]["text"],
            "score": cosine_similarities[i],
            "filepath": files[i]["filepath"]
        })

    return result

def check_files():
    global files, args
    while True:
        # Get the list of all files in the docpath
        files_on_disk = [os.path.join(root, file) 
                 for root, dirs, files in os.walk(args.docpath) 
                 for file in files]

        # Check for file modifications and new files
        for file in files_on_disk:
            last_modified = datetime.datetime.fromtimestamp(os.stat(file).st_mtime)
            for item in files:
                if item['filepath'] == file:
                    # Update last_modified and content if file is modified
                    if item['last_modified'] < last_modified:
                        item['last_modified'] = last_modified
                        print(f"{file} was updated, reloading it")
                        with open(file, 'r') as f:
                            item['text'] = f.read()
                    break
            else:  # If file is not in data, add it
                print(f"{file} is a new file, adding it")
                with open(file, 'r') as f:
                    text = f.read()
                files.append({
                    'filepath': file,
                    'last_modified': last_modified,
                    'text': text
                })

        # Check for deleted files
        files = [item for item in files if item['filepath'] in files_on_disk]
        time.sleep(5)  # Wait for 5 seconds before the next check
    
files = []

def main():
    global args, files
    parser = argparse.ArgumentParser(description='Serve a plugin API for GPT-4, serving project drfinitions and descriptions')
    parser.add_argument("--docpath", required=True, help="the directory where the definitions and descriptions will be stored")    
    parser.add_argument("--name", required=True, help="name of the project")    
    parser.add_argument("--port", required=False, help="port to serve on", default=5002)    
    args = parser.parse_args()
    monitoring_thread = threading.Thread(target=check_files)
    monitoring_thread.start()
    app.run(debug=True, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()