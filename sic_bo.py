# This example is provided for informational purposes only and has not been audited for security.

from pyteal import *


@Subroutine(TealType.uint64)
def checkOne(dice1, dice2, dice3, val):
    return Or(dice1 == val, dice2 == val, dice3 == val)


@Subroutine(TealType.uint64)
def checkTwo(dice1, dice2, dice3, val1, val2):
    return If(val1 != val2).Then(
        Return(
            And(checkOne(dice1, dice2, dice3, val1),
                checkOne(dice1, dice2, dice3, val2)))).Else(
                    Return(checkDouble(dice1, dice2, dice3, val1)))


@Subroutine(TealType.uint64)
def getSum(dice1, dice2, dice3):
    return dice1 + dice2 + dice3


@Subroutine(TealType.uint64)
def checkSum(dice1, dice2, dice3, sum):
    return getSum(dice1, dice2, dice3) == sum


@Subroutine(TealType.uint64)
def checkSumRange(dice1, dice2, dice3, lower, upper):
    return And(
        getSum(dice1, dice2, dice3) >= lower,
        getSum(dice1, dice2, dice3) <= upper)


@Subroutine(TealType.uint64)
def countNumVal(dice1, dice2, dice3, val):
    return dice1 == val + dice2 == val + dice3 == val


@Subroutine(TealType.uint64)
def checkDouble(dice1, dice2, dice3, val):
    return countNumVal(dice1, dice2, dice3, val) >= Int(2)


@Subroutine(TealType.uint64)
def checkTriple(dice1, dice2, dice3, val):
    return countNumVal(dice1, dice2, dice3, val) == Int(3)


@Subroutine(TealType.uint64)
def checkAnyTriple(dice1, dice2, dice3):
    return dice1 == dice2 == dice3


@Subroutine(TealType.uint64)
def matchBet(type, val1, val2, dice1, dice2, dice3):
    return Cond(
        [type == Bytes("one"),
         Return(checkOne(dice1, dice2, dice3, val1))], [
             type == Bytes("two"),
             Return(checkTwo(dice1, dice2, dice3, val1, val2))
         ],
        [type == Bytes("sum"),
         Return(checkSum(dice1, dice2, dice3, val1))], [
             type == Bytes("sum_range_small"),
             Return(checkSumRange(dice1, dice2, dice3, Int(4), Int(10)))
         ], [
             type == Bytes("sum_range_big"),
             Return(checkSumRange(dice1, dice2, dice3, Int(11), Int(17)))
         ], [
             type == Bytes("double"),
             Return(checkDouble(dice1, dice2, dice3, val1))
         ], [
             type == Bytes("triple"),
             Return(checkTriple(dice1, dice2, dice3, val1))
         ], [
             type == Bytes("any_triple"),
             Return(checkAnyTriple(dice1, dice2, dice3))
         ])


def approval_program():
    dice1 = ScratchVar(TealType.uint64)
    dice2 = ScratchVar(TealType.uint64)
    dice3 = ScratchVar(TealType.uint64)
    bet = Seq([
        dice1.store(Int(1)),
        dice2.store(Int(4)),
        dice3.store(Int(5)),
        App.globalPut(
            Bytes("result"),
            matchBet(Txn.application_args[1], Btoi(Txn.application_args[2]),
                     Btoi(Txn.application_args[3]),
                     Btoi(Txn.application_args[4]),
                     Btoi(Txn.application_args[5]),
                     Btoi(Txn.application_args[6]))),
        Return(Int(1)),
    ])

    test = Seq([App.globalPut(Bytes("test"), Int(6969)), Return(Int(1))])

    program = Cond(
        [Txn.application_id() == Int(0),
         Return(Int(1))],
        [Txn.on_completion() == OnComplete.OptIn,
         Return(Int(1))],
        [Txn.application_args[0] == Bytes("bet"), bet],
        [Txn.application_args[0] == Bytes("test"), test],
    )

    return program


def clear_state_program():
    program = Seq([
        Return(Int(1)),
    ])

    return program


if __name__ == "__main__":
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(),
                               mode=Mode.Application,
                               version=4)
        f.write(compiled)

    with open("clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(),
                               mode=Mode.Application,
                               version=4)
        f.write(compiled)
