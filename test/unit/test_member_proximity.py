import pytest

from member_proximity import clean_address


@pytest.mark.parametrize(
    "problem_address, cleaned_address",
    [
        (
            "1111 NW 82nd St. Apt. #11 City, State 11125",
            "1111 NW 82nd St. City, State 11125",
        ),
        (
            "1111 NW 86th St Apt 16 City, State 11122",
            "1111 NW 86th St City, State 11122",
        ),
        (
            "1111 SE Fake Dr Unit 5 City, State 11111-5084",
            "1111 SE Fake Dr City, State 11111",
        ),
        (
            "1111 Canterbury Rd Apt 172 City, State 11122-4624",
            "1111 Canterbury Rd City, State 11122",
        ),
        (
            "1111 Jack London Drive City, State 11131-1596",
            "1111 Jack London Drive City, State 11131",
        ),
        ("1111 Winwood Dr #108 City, State 11131", "1111 Winwood Dr City, State 11131"),
        ("1111 Gables Way City, State 11131-3025", "1111 Gables Way City, State 11131"),
        (
            "1111 Patricia Dr Apt 502 City, State 11122-5260",
            "1111 Patricia Dr City, State 11122",
        ),
        (
            "1111 Merle Hay Rd Unit 305 City, State 11131-1476",
            "1111 Merle Hay Rd City, State 11131",
        ),
        (
            "1111 Iltis Dr Apt F58 City, State 11122-1627",
            "1111 Iltis Dr City, State 11122",
        ),
        (
            "1111 Iltis Dr Bldg L City, State 11122-1620",
            "1111 Iltis Dr City, State 11122",
        ),
        (
            "1111 NW 103rd Lane City, State 11111",
            "1111 NW 103rd Lane City, State 11111",
        ),
        (
            "1111 Hazelwood Ave City, State 11131-3019",
            "1111 Hazelwood Ave City, State 11131",
        ),
        (
            "1111 S.E. Freedom Dr. City, State 11111",
            "1111 S.E. Freedom Dr. City, State 11111",
        ),
        (
            "11111 Douglas Ave # 213 City, State 11122",
            "11111 Douglas Ave City, State 11122",
        ),
        (
            "1111 NW 106th St Apt 207 City, State 11131-2466",
            "1111 NW 106th St City, State 11131",
        ),
        ("1111 Patricia Ave, Apt 35 City, State", "1111 Patricia Ave City, State"),
        (
            "1111 Nw Country Club Dr. City, State 11122",
            "1111 Nw Country Club Dr. City, State 11122",
        ),
    ],
)
def test_clean_addresses(problem_address, cleaned_address):
    assert cleaned_address == clean_address(problem_address)
