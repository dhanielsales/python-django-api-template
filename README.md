Goals

- Have a more linear file organization, in order to make the direction of consumption flow clear and each layer works in isolation. (Separation of concerns and dependency inversion principle)
- Reorganize and centralize database interactions, making it possible to add specific behaviors after an action, while still making maintenance easy
- Make tests easier to be built

Topics

- `*_test.py` files
- split usecase files
- the entity and repository idea
- linearity of API consumption
  - View -> usecase -> repository -> entity --- entity -> repository -> usecase -> view
- Show problems with stub but also advantages with type anotations on models
