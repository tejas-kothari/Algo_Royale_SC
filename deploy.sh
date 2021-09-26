export ADDR_CREATOR="B7JMEWPVRTE6VSFDNFG4OZC7KO7HLTYSTUU5GYXGQPZCHL5CVSYK5ANTBE"

export TEAL_APPROVAL_PROG="approval.teal"
export TEAL_CLEAR_PROG="clear_state.teal"

export GLOBAL_BYTESLICES=2
export GLOBAL_INTS=1
export LOCAL_BYTESLICES=2
export LOCAL_INTS=0

python sic_bo.py

./sandbox/sandbox reset

./sandbox/sandbox copyTo "$TEAL_APPROVAL_PROG"
./sandbox/sandbox copyTo "$TEAL_CLEAR_PROG"

./sandbox/sandbox goal app create \
--approval-prog "$TEAL_APPROVAL_PROG" --clear-prog "$TEAL_CLEAR_PROG" \
--creator $ADDR_CREATOR \
--global-byteslices $GLOBAL_BYTESLICES \
--global-ints $GLOBAL_INTS \
--local-byteslices $LOCAL_BYTESLICES \
--local-ints $LOCAL_INTS

./sandbox/sandbox goal clerk send -a 1000000 -f $ADDR_CREATOR -t H7ZH3Z2JJPFON5CRHPDQDBTC5MR2HYSHHLVGKPU2JQZQ2XIRQHXMAHY5UE