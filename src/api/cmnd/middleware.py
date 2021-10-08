from src.utils.error_handle import Exception_Handle


def check_value_scaned_is_none(success):
    if not success:
        raise Exception_Handle(
            result=False,
            step=2,
            message="some value scaned is none",
            code=200,
            field="",
            name=__name__
        )
