import requests

def test_fetch():
    r = requests.get("http://127.0.0.1:8000/api/video?letter=A", stream=True)
    print("status:", r.status_code)
    # save first bytes to file if ok
    if r.status_code == 200:
        with open("sample_A.mp4", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("saved sample_A.mp4")