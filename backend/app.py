from flask import Flask, jsonify
from flask.logging import create_logger
import json
import logging
import os
import psycopg2

connection = psycopg2.connect(dbname = os.environ["DATABASE_NAME"],
                              user = os.environ["DATABASE_USERNAME"],
                              password = os.environ["DATABASE_PASSWORD"],
                              host = os.environ["DATABASE_HOST"],
                              port = os.environ["DATABASE_PORT"])

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # Query for random wisdom
    cursor.execute("SELECT * FROM Wisdoms ORDER BY random() LIMIT 1")
    # Retrieve query results
    records = cursor.fetchall()
    id_ = records[0][0]
    wisdom = records[0][1]
    source = records[0][2]
    LOG.info(f"Wisdom: \n{wisdom}")
    LOG.info(f"Source: \n{source}")

    # Query for wisdom categories
    cursor.execute("SELECT category FROM Categories WHERE wisdomId = '" + str(id_) + "'")
    categories_sql = cursor.fetchall()
    categories = []
    for c in categories_sql:
        categories.append(c[0])
    LOG.info(f"Categories:")
    LOG.info(f"{categories}")

    # Query for image urls
    cursor.execute("SELECT imageUrl FROM Images WHERE wisdomId = '" + str(id_) + "'")
    imageUrls_sql = cursor.fetchall()
    imageUrls = []
    for u in imageUrls_sql:
        imageUrls.append(u[0])
    LOG.info(f"Image URLs:")
    LOG.info(f"{imageUrls}")
    cursor.close()

    ## Activate if backend should directly display results in html
    #html = f"<h1>GetWise</h1>\n\n"
    #html += f"<pre>" + wisdom + "</pre>\n\n"
    #if source:
    #    html += f"<p>Source: " + source + "</p>\n\n"
    #if categories:
    #    html += f"<p>Categories:</p>\n"
    #for c in categories:
    #    html += f"<p>" + c + "</p>\n"
    #for u in imageUrls:
    #    html += f"<img src=\"" + u + "\">\n"
    #return html.format(format)
        
    return jsonify({"wisdom": wisdom, "source": source, "categories": json.dumps(categories), "img-urls": json.dumps(imageUrls)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
