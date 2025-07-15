from infra.celery.app import app

# TODO: Implement actual event emission logic
# Ideally it should be an interface using `typing.Protocol`,
# to be properly injected into the repository.

# Celery uses the same context to issue and receive an asynchronous operation,
# so I chose to group everything in /tasks. In another scenario, we would have
# `src/application/presentation/deals/listener.py` and `src/application/emitters/deals/`.


@app.task
def deal_created_emitter(deal_id: int) -> None:
    """Emit an event when a deal is created."""
    print(f"Deal created event emitted for deal_id={deal_id}")


@app.task
def deal_updated_emitter(deal_id: int) -> None:
    """Emit an event when a deal is updated."""
    print(f"Deal updated event emitted for deal_id={deal_id}")


@app.task
def deal_deleted_emitter(deal_id: int) -> None:
    """Emit an event when a deal is deleted."""
    print(f"Deal deleted event emitted for deal_id={deal_id}")
