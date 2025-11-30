# ASL Video API (Images -> Video)

This project demonstrates a simple MVC-style FastAPI application that:
- Stores ASL images in `asl_alphabet/<LETTER>/`
- Provides an endpoint `/api/video?letter=<LETTER>` which:
  - Loads images for the requested letter
  - Assembles them into an MP4 video (1 second per frame by default)
  - Returns the video as a streaming response (`video/mp4`)

## Structure

```
app/
  routes/
    sign_route.py
  models/
    sign_model.py
  views/
    response_view.py
asl_alphabet/
  A/
    A1.jpg
    A2.jpg
    ...
  B/
  ...
requirements.txt
```

## How to run locally

1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows use: .\.venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Test in your browser or with curl:
   - Video for letter A:
     ```
     http://127.0.0.1:8000/api/video?letter=A
     ```
   - Special words:
     ```
     http://127.0.0.1:8000/api/video?letter=space
     http://127.0.0.1:8000/api/video?letter=del
     http://127.0.0.1:8000/api/video?letter=nothing
     ```

## Notes

- The project currently uses **local** `asl_alphabet` folder bundled in the repo containing placeholder images.
- If you want the API to download images from a GitHub repo instead, replace the model code to fetch images (raw) from GitHub and store them temporarily before creating the video.
- FPS (frames per second) and other video params can be adjusted in `create_video_for_letter`.