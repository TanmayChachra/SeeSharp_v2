from website import create_app,remove_contents,UPLOAD_FOLDER

app = create_app()

if __name__ == '__main__':
    remove_contents(UPLOAD_FOLDER)
    remove_contents("website\\static\\results")
    app.run(debug=True)
