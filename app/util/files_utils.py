import uuid

from github import InputGitTreeElement, Github
import base64

from config import Config


def upload_image(filename):
    try:
        g = Github(Config.GITHUB_TOKEN)
        repo = g.get_user().get_repo(Config.GITHUB_REPO)
        branch = repo.get_branch("main")

        # Genera un hash único para el nombre del archivo
        unique_filename = f"{uuid.uuid4()}_{filename}"

        # Asegúrate de que el archivo está en el lugar correcto y tiene el nombre correcto.
        image_path = f'app/static/images/{filename}'
        with open(image_path, 'rb') as image_file:
            # GitHub espera que el contenido del archivo binario sea base64 codificado.
            content = base64.b64encode(image_file.read())

        # Crea un objeto GitBlob que represente el archivo binario.
        git_blob = repo.create_git_blob(content.decode('utf-8'), "base64")

        # Crea un árbol con el nuevo blob y el árbol actual de la rama para mantener otros archivos.
        base_tree = repo.get_git_tree(branch.commit.sha)
        element = InputGitTreeElement(path=unique_filename, mode='100644', type='blob', sha=git_blob.sha)
        tree = repo.create_git_tree([element], base_tree)

        # Crea un nuevo commit en la rama.
        parent = repo.get_git_commit(branch.commit.sha)
        commit = repo.create_git_commit("Subida de imagen con nombre único", tree, [parent])
        ref = repo.get_git_ref(f'heads/{branch.name}')
        ref.edit(sha=commit.sha)
        image_url = f"https://raw.githubusercontent.com/{Config.GITHUB_REPO}/main/app/static/images/{unique_filename}"
        return image_url

    except Exception as e:
        print(f"Error al subir la imagen a GitHub: {e}")
        return None
