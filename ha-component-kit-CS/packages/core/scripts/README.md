#### Local Development - sync-ha-types
The typesync script is under packages/core/scripts/sync-ha-types
This script is responsible for syncing types that are defined in the home assistant repository, it saves having to manage things that may change with time

1. Set your directory to ./packages/core
2. Run the following:

```shell
npm run build:sync-ha-types
```
This may not do anything depending on the changes, if things have changed you should see the autogenerated-types-by-domain.ts updated in your git log.

If you want to extend or change the default values used by a certain domain/entity, you can edit the src/types/entities or entitiesByDomain files which will reflect across hooks and components.

An example would be to look at the Vacuum entity which has a custom state property under entitiesByDomain/index.ts


#### Local Development - sync-user-types
The typesync script is under packages/core/scripts
This script is responsible for generating types for users for the home assistant instance, there's a node and cli script available, the cli script imports the node script for simplicity.

1. Run `npm link -ws` at the root level of ha-component-kit
2. Set your directory to ./packages/core
3. Run the following:

```shell
npm run watch:build:sync-script
```
4. on your test dashboard, run `npm link @hakit/core`
5. Follow the steps to setup the sync script on the test dashboard [here](https://shannonhochkins.github.io/ha-component-kit/?path=/docs/introduction-typescriptsync--docs)
6. Now when you run the sync script you'll see your changes reflect in the node version only, the cli script will not re-compile here.

NOTE: In watch mode the types will not be re-generated on subsequent changes, you will have to kill the terminal and restart it.