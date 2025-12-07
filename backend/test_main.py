"""Unit tests for HomeBuh API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from .db import get_session
from .main import app
from .models import Category, Account, Transaction, Budget, PlannedItem


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with mocked database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestHealth:
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCategories:
    def test_create_category(self, client: TestClient):
        """Test creating a new category."""
        response = client.post(
            "/api/categories",
            json={"name": "Продукты", "parent_id": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Продукты"
        assert data["id"] is not None

    def test_list_categories(self, client: TestClient):
        """Test listing all categories."""
        # Create a category first
        client.post("/api/categories", json={"name": "Категория 1"})
        response = client.get("/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["name"] == "Категория 1"

    def test_create_subcategory(self, client: TestClient):
        """Test creating a subcategory."""
        # Create parent
        parent_resp = client.post("/api/categories", json={"name": "Родитель"})
        parent_id = parent_resp.json()["id"]

        # Create child
        response = client.post(
            "/api/categories",
            json={"name": "Подкатегория", "parent_id": parent_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parent_id"] == parent_id


class TestAccounts:
    def test_create_account(self, client: TestClient):
        """Test creating a new account."""
        response = client.post(
            "/api/accounts",
            json={"name": "Мой кошелек", "balance": 1000.0, "currency": "USD"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Мой кошелек"
        assert data["balance"] == 1000.0

    def test_list_accounts(self, client: TestClient):
        """Test listing all accounts."""
        client.post("/api/accounts", json={"name": "Счет 1", "balance": 500})
        response = client.get("/api/accounts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    def test_account_default_currency(self, client: TestClient):
        """Test that account defaults to USD currency."""
        response = client.post(
            "/api/accounts",
            json={"name": "Счет", "balance": 0}
        )
        data = response.json()
        assert data["currency"] == "USD"


class TestTransactions:
    def test_create_transaction(self, client: TestClient):
        """Test creating a transaction."""
        # Create account and category first
        acc_resp = client.post("/api/accounts", json={"name": "Acc", "balance": 1000})
        acc_id = acc_resp.json()["id"]
        cat_resp = client.post("/api/categories", json={"name": "Cat"})
        cat_id = cat_resp.json()["id"]

        # Create transaction
        response = client.post(
            "/api/transactions",
            json={
                "amount": -50.0,
                "currency": "USD",
                "description": "Тестовая транзакция",
                "account_id": acc_id,
                "category_id": cat_id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == -50.0
        assert data["description"] == "Тестовая транзакция"

    def test_list_transactions(self, client: TestClient):
        """Test listing transactions."""
        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestBudgets:
    def test_create_budget(self, client: TestClient):
        """Test creating a budget."""
        # Create category
        cat_resp = client.post("/api/categories", json={"name": "Cat"})
        cat_id = cat_resp.json()["id"]

        response = client.post(
            "/api/budgets",
            json={
                "year_month": "2025-12",
                "category_id": cat_id,
                "amount": 500.0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["year_month"] == "2025-12"
        assert data["amount"] == 500.0

    def test_list_budgets(self, client: TestClient):
        """Test listing budgets."""
        response = client.get("/api/budgets")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestPlannedItems:
    def test_create_planned_item(self, client: TestClient):
        """Test creating a planned item."""
        cat_resp = client.post("/api/categories", json={"name": "Cat"})
        cat_id = cat_resp.json()["id"]

        response = client.post(
            "/api/planned",
            json={
                "title": "Планируемый расход",
                "amount": 200.0,
                "type": "expense",
                "category_id": cat_id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Планируемый расход"
        assert data["type"] == "expense"

    def test_list_planned_items(self, client: TestClient):
        """Test listing planned items."""
        response = client.get("/api/planned")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestTransfer:
    def test_successful_transfer(self, client: TestClient):
        """Test successful account transfer."""
        # Create two accounts
        acc1 = client.post("/api/accounts", json={"name": "A1", "balance": 500}).json()
        acc2 = client.post("/api/accounts", json={"name": "A2", "balance": 100}).json()

        # Transfer
        response = client.post(
            "/api/transfer",
            json={
                "from_account_id": acc1["id"],
                "to_account_id": acc2["id"],
                "amount": 100.0,
                "currency": "USD"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["from_tx"]["amount"] == -100.0
        assert data["to_tx"]["amount"] == 100.0

    def test_transfer_insufficient_funds(self, client: TestClient):
        """Test transfer with insufficient funds."""
        acc1 = client.post("/api/accounts", json={"name": "A1", "balance": 10}).json()
        acc2 = client.post("/api/accounts", json={"name": "A2", "balance": 0}).json()

        response = client.post(
            "/api/transfer",
            json={
                "from_account_id": acc1["id"],
                "to_account_id": acc2["id"],
                "amount": 100.0
            }
        )
        assert response.status_code == 400
        assert "insufficient funds" in response.json()["detail"].lower()

    def test_transfer_same_account(self, client: TestClient):
        """Test that transfer to same account is rejected."""
        acc = client.post("/api/accounts", json={"name": "A", "balance": 100}).json()

        response = client.post(
            "/api/transfer",
            json={
                "from_account_id": acc["id"],
                "to_account_id": acc["id"],
                "amount": 50.0
            }
        )
        assert response.status_code == 400
        assert "must differ" in response.json()["detail"].lower()

    def test_transfer_negative_amount(self, client: TestClient):
        """Test that negative amount is rejected."""
        acc1 = client.post("/api/accounts", json={"name": "A1", "balance": 100}).json()
        acc2 = client.post("/api/accounts", json={"name": "A2", "balance": 0}).json()

        response = client.post(
            "/api/transfer",
            json={
                "from_account_id": acc1["id"],
                "to_account_id": acc2["id"],
                "amount": -50.0
            }
        )
        # Should be rejected by Pydantic validation (gt=0)
        assert response.status_code == 422


class TestAIChat:
    def test_ai_chat_without_openai_key(self, client: TestClient):
        """Test AI chat endpoint without OpenAI key (fallback)."""
        response = client.post(
            "/api/ai/chat",
            json={"prompt": "Тестовый запрос"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "charts" in data
        assert isinstance(data["charts"], list)

    def test_ai_chat_empty_prompt(self, client: TestClient):
        """Test AI chat with empty prompt."""
        response = client.post(
            "/api/ai/chat",
            json={"prompt": ""}
        )
        assert response.status_code == 400
