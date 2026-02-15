import pandas as pd
from flask import Flask, request, render_template
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

### Format the data for the UI
async def format_data(retrieved_data, resolutions):
    reduction = 0
    if retrieved_data['old_total'] > 0:
        reduction = round(
            (1 - (retrieved_data['new_total'] / retrieved_data['old_total'])) * 100
        )

    resolutions_new = []
    for name, count in resolutions.items():
        resolutions_new.append({
            "name": name, "count": count
        })
    
    return {
        "totalSize": round(retrieved_data['old_total']*1024*1024*1024, 2),
        "compressedSize": round(retrieved_data['new_total']*1024*1024*1024, 2),
        "dataSaved": round((retrieved_data['old_total'] - retrieved_data['new_total'])*1024*1024*1024, 2),
        "reduction": reduction,
        "uncompressedCount": retrieved_data['unencoded_total'],
        "compressedCount": retrieved_data['encoded_total'],
        "resolutions": resolutions_new
    }

@app.route("/stats", methods=['POST']) 
async def get_stats():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    
    # Read the CSV content from the uploaded file
    csv_data = file.stream.read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_data), index_col=0)

    retrieved_data = {
        "old_total": 0,
        "new_total": 0,
        "unencoded_total": 0,
        "encoded_total": 0
    }
    
    resolutions = {
        "4k": 0,
        "1080p": 0,
        "720p": 0,
        "480p": 0,
        "Other": 0
    }

    codecs = {

    }

    df = df.reset_index()
    for _, row in df.iterrows():
        try:
            if len(row) == 32:
                retrieved_data["old_total"] += row['oldSize']
                retrieved_data["new_total"] += row['newSize']
                if row['newVsOldRatio'] == 100:
                    retrieved_data["unencoded_total"] += 1
                else:
                    retrieved_data["encoded_total"] += 1
            match row['video_resolution']:
                case "4KUHD":
                    resolutions["4k"] += 1
                case "1080p":
                    resolutions["1080p"] += 1
                case "720p":
                    resolutions["720p"] += 1
                case "480p":
                    resolutions["480p"] += 1
                case _:
                    resolutions["Other"] += 1
        except:
            print("Issue with row (invalid data)")

    return await format_data(retrieved_data, resolutions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)