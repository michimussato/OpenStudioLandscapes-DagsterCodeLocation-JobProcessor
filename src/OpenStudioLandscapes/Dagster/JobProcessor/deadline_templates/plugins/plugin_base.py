args = list()

plugin = {
    "submitter":
    {
        "executable": None,
        "output_formats_plugin": ["png", "exr", "jpg"],
        "args": args,
        "padding_deadline": "'#' * EVAL_PADDING",  # results in "####"
        "padding_command": "'#' * EVAL_PADDING",   # results in "####"
    }
}
