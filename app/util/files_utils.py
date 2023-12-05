from github import InputGitTreeElement, Github
import base64

from config import Config


# Upload an image to GitHub
def upload_image(filename):
    try:
        g = Github(Config.GITHUB_TOKEN)
        repo = g.get_user().get_repo(Config.GITHUB_REPO)
        branch = repo.get_branch("main")

        with open(f'app/static/images/{filename}', 'rb') as file:
            content = file.read()
            content_base64 = base64.b64encode(content).decode()

        git_file = f'static/images/{filename}'
        element = InputGitTreeElement(git_file, '100644', 'blob', content_base64)
        tree = repo.create_git_tree([element], repo.get_git_tree(branch.commit.sha))
        parent = repo.get_git_commit(branch.commit.sha)
        commit = repo.create_git_commit("Subida de imagen", tree, [parent])

        # Actualiza la rama con el nuevo commit
        ref = f'refs/heads/{branch.name}'
        repo.get_git_ref(ref[5:]).edit(commit.sha)

    except Exception as e:
        print(f"Error al subir la imagen a GitHub: {e}")
