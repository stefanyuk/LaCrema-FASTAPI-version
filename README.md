#### API schemas naming conventions:
1. Each model should be named according to the business entity it represents. e.g.: `User`, `Team`.
2. A model which represents a persisted entity (usually that's the minimal set of fields + the `id`) must have the
`Existing` suffix e.g.: `ExistingDepartment`, `ExistingUser`.
3. A model which describes all the available fields of an entity must have the `Extended` suffix e.g. `ExtendedDepartment`,
`ExtendedUser`.
4. A model which describes API input must have suffix `In`, e.g.: `UserIn`, `DepartmentIn`
5. A model which describes the API output must have suffix `Out`, e.g.: `UserOut`,
`DepartmentOut`.
6. A model which describes the collection API output must follow the following naming convention: `CollectionOut`
e.g.: `UserCollectionOut`, `TeamExtendedCollectionOut`.
7. In order to create embedded API output, `Embed` suffix must be used, e.g.: `EmbedUserOut`.
