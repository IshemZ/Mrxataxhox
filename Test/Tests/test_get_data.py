import pytest
from unittest.mock import patch, MagicMock
from get_data import get_pages 

# Mock de constantes
DATABASE_ID = "mock_database_id"
NOTION_API_KEY = "mock_api_key"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture pour simuler les variables d'environnement."""
    monkeypatch.setenv("NOTION_API_KEY", NOTION_API_KEY)
    monkeypatch.setenv("DATABASE_ID", DATABASE_ID)

@patch("your_module.requests.post")
def test_get_pages_all(mock_post, mock_env):
    # Mock de la réponse de l'API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"id": "page_1"}, {"id": "page_2"}],
        "has_more": False
    }
    mock_post.return_value = mock_response

    # Appeler la fonction
    pages = get_pages()

    # Vérifier les résultats
    assert len(pages) == 2
    assert pages[0]["id"] == "page_1"
    assert pages[1]["id"] == "page_2"

    # Vérifier que l'API a été appelée correctement
    mock_post.assert_called_once_with(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
        json={"page_size": 100},
        headers=headers
    )

@patch("your_module.requests.post")
def test_get_pages_with_limit(mock_post, mock_env):
    # Mock de la réponse de l'API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"id": "page_1"}],
        "has_more": False
    }
    mock_post.return_value = mock_response

    # Appeler la fonction avec une limite
    pages = get_pages(num_pages=1)

    # Vérifier les résultats
    assert len(pages) == 1
    assert pages[0]["id"] == "page_1"

    # Vérifier que l'API a été appelée correctement
    mock_post.assert_called_once_with(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
        json={"page_size": 1},
        headers=headers
    )

@patch("your_module.requests.post")
def test_get_pages_pagination(mock_post, mock_env):
    # Mock de la première réponse avec pagination
    mock_response_1 = MagicMock()
    mock_response_1.json.return_value = {
        "results": [{"id": "page_1"}],
        "has_more": True,
        "next_cursor": "cursor_1"
    }

    # Mock de la deuxième réponse
    mock_response_2 = MagicMock()
    mock_response_2.json.return_value = {
        "results": [{"id": "page_2"}],
        "has_more": False
    }

    # Configurer le side_effect pour retourner plusieurs réponses
    mock_post.side_effect = [mock_response_1, mock_response_2]

    # Appeler la fonction
    pages = get_pages()

    # Vérifier les résultats
    assert len(pages) == 2
    assert pages[0]["id"] == "page_1"
    assert pages[1]["id"] == "page_2"

    # Vérifier que l'API a été appelée deux fois
    assert mock_post.call_count == 2

@patch("your_module.requests.post")
def test_get_pages_error(mock_post, mock_env):
    # Mock d'une réponse avec erreur
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid request"}
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    # Vérifier que la fonction gère l'erreur
    with pytest.raises(KeyError):  # Suppose qu'une clé manquante dans le JSON lève une exception
        get_pages()
