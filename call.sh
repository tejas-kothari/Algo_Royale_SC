export APP_ID=1
export ADDR_CREATOR="B7JMEWPVRTE6VSFDNFG4OZC7KO7HLTYSTUU5GYXGQPZCHL5CVSYK5ANTBE"

./sandbox/sandbox goal app optin --app-id $APP_ID --from $ADDR_CREATOR

./sandbox/sandbox goal app call --app-id $APP_ID --from $ADDR_CREATOR \
--app-arg "str:bet" --app-arg "str:two" --app-arg "int:4" --app-arg "int:5" --app-arg "int:1" --app-arg "int:4" --app-arg "int:5"

./sandbox/sandbox goal app read --app-id $APP_ID --guess-format --global --from $ADDR_CREATOR