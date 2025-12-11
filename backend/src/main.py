# main.py

import uvicorn


def main():
    uvicorn.run(
        app="app:app", host="localhost", port=8080, reload=True
    )  # app.py의 app 모듈을 쓰겠다는 뜻


if __name__ == "__main__":
    main()
