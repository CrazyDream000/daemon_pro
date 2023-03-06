import builtins
import json
import traceback

from typing import Optional


class RipFunCall:
    @staticmethod
    def wrap_fun(fun: builtins, *args, **kwargs) -> tuple:
        """
        fun:argument function name without parenthesis
        *args:argument unname params as tuple ("cat",13,12.2)
        +*kwargs:argument named params as dictionary {"path":"/my-drive"}
        """

        res = None
        err = None
        if fun is None:
            # print("NONE FUN")
            err = ("Null function", "Null function")
        else:
            try:
                # print("FUN: " + fun.__name__ + " ARGS: " + str(args) + " KWARGS " + str(kwargs))
                # print("plain args " + str(args))
                # print("plain kwargs " + str(kwargs))
                if args == ():
                    # print("plain call " + str(fun()))
                    res = {str(fun.__name__): fun()}
                    # print("!!!!! FUN: " + fun.__name__ + " R/E: " + json.dumps(res))
                elif args != () and kwargs == {}:
                    # print("DELLA M " + str(fun.__name__))
                    res = {str(fun.__name__): fun(*args)}
                    # print("!!!!! FUN: " + fun.__name__ + " R/E: " + json.dumps(res))
                    # print("DEL M " + str(fun.__name__) + " END")
                elif args == (None,) and kwargs != {}:
                    # print("DELLA S " + str(fun.__name__))
                    res = {str(fun.__name__): fun(**kwargs["kwargs"])}
                    # print("!!!!! FUN: " + fun.__name__ + " R/E: " + json.dumps(res))
                    # print("DEL S " + str(fun.__name__) + " END")
                elif args != (None,) and kwargs != {}:
                    # print("DEL C " + str(fun.__name__))
                    res = {str(fun.__name__): fun(*args, **kwargs["kwargs"])}
                    # print("!!!!! FUN: " + fun.__name__ + " R/E: " + json.dumps(res))
                    # print("DEL C " + str(fun.__name__) + " END")

            except Exception as exc:
                # print("DEL SEGUGIO " + str(fun.__name__) + "EXCEPTION" + str(exc))
                err = (str(fun.__name__), str(exc))
        return res, err

    @staticmethod
    def wrap_fun_array_duplicate_rename(fun_arr: list) -> Optional[dict]:
        res = {}
        seen_functions = {}
        if fun_arr is None:
            return None
        if len(fun_arr) < 1:
            res["status"] = "Empty fun array"
        i = 0

        for fun in fun_arr:
            try:
                # print(type(fun))
                the_fun = None
                fun_key = ""
                fun_args_wargs = None
                if callable(fun):
                    # print("BUILTIN: " + fun.__name__)
                    fun_key = str(fun.__name__)
                    the_fun = fun
                elif type(fun) is tuple:
                    # print("ID: " + str(i) + " IS TUPLE ")
                    if len(fun) < 2 or len(fun) > 3:
                        res["err_elem_" + str(i)] = "incorrect number of parameters for element " + str(
                            i) + " in the function array"
                    else:
                        if callable(fun[0]):
                            fun_key = str(fun[0].__name__)
                            the_fun = fun[0]
                            fun_args_wargs = fun[1:]

                            # r, e = RipFunCall.wrap_fun(fun[0], fun[1:])
                            # print("r: " + str(r) + " e: " + str(e))
                if the_fun is not None:
                    if fun_key is not None:
                        r = None
                        e = None
                        if fun_args_wargs is not None:
                            if len(fun_args_wargs) == 1:
                                # print("RUN 1 " + str(fun_args_wargs))
                                r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs[0])
                            elif len(fun_args_wargs) == 2:
                                # print("RUN 2 " + str(fun_args_wargs))
                                r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs[0], kwargs=fun_args_wargs[1])
                                # r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs)
                            else:
                                res["err_elem_" + str(i)] = "inconsistent args call"
                        else:
                            r, e = RipFunCall.wrap_fun(the_fun)
                        if fun_key in seen_functions.keys():
                            seen_functions[fun_key] += 1
                        else:
                            seen_functions[fun_key] = 0
                        fun_name = str(fun_key) + "!" + str(seen_functions[fun_key])
                        res[fun_name] = {
                            "call": fun_key,
                            "id": fun_name,
                            "result": r,
                            "errors": str(e),
                            "args": str(fun_args_wargs),
                            "client_call_array_id": i
                        }
                    else:
                        res["err_elem_" + str(i)] = "null function key"
                else:
                    res["err_elem_" + str(i)] = "null function"
            except Exception as exc:
                res["err_elem_" + str(i)] = traceback.print_exception(type(exc), exc, exc.__traceback__)
                # for ex in exc:
                #     res["err_elem_" + str(i)] += res["err_elem_" + str(i)] \
                #                                  + " | " + traceback.print_exception(type(ex),
                #                                                                      exc,
                #                                                                      exc.__traceback__)
                # res["err_elem_" + str(i)] = str(exc) + " track " + str(exc.with_traceback())
            i += 1
        return res

    @staticmethod
    def safe_wrap_fun_array_duplicate_rename(fun_arr: list) -> Optional[dict]:
        res = {}
        seen_functions = {}
        if fun_arr is None:
            return None
        if len(fun_arr) < 1:
            res["status"] = "Empty fun array"
        i = 0

        for fun_1 in fun_arr:
            if type(fun_1) is tuple and len(fun_1) > 1:
                try:
                    try:
                        if len(fun_1) == 2:
                            fun = getattr(fun_1[0], fun_1[1])
                        else:
                            fun = (getattr(fun_1[0], fun_1[1]),) + fun_1[2:]
                    except AttributeError as at:
                        res["err_elem_" + str(i)] = "unsupporte function call " + str(at)

                    print(str(fun))
                    the_fun = None
                    fun_key = ""
                    fun_args_wargs = None
                    if callable(fun):
                        # print("BUILTIN: " + fun.__name__)
                        fun_key = str(fun.__name__)
                        the_fun = fun
                    elif type(fun) is tuple:
                        # print("ID: " + str(i) + " IS TUPLE ")
                        if len(fun) < 2 or len(fun) > 3:
                            res["err_elem_" + str(i)] = "incorrect number of parameters for element " + str(
                                i) + " in the function array"
                        else:
                            if callable(fun[0]):
                                fun_key = str(fun[0].__name__)
                                the_fun = fun[0]
                                fun_args_wargs = fun[1:]

                                # r, e = RipFunCall.wrap_fun(fun[0], fun[1:])
                                # print("r: " + str(r) + " e: " + str(e))
                    if the_fun is not None:
                        if fun_key is not None:
                            r = None
                            e = None
                            if fun_args_wargs is not None:
                                if len(fun_args_wargs) == 1:
                                    # print("RUN 1 " + str(fun_args_wargs))
                                    r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs[0])
                                elif len(fun_args_wargs) == 2:
                                    # print("RUN 2 " + str(fun_args_wargs))
                                    r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs[0], kwargs=fun_args_wargs[1])
                                    # r, e = RipFunCall.wrap_fun(the_fun, fun_args_wargs)
                                else:
                                    res["err_elem_" + str(i)] = "inconsistent args call"
                            else:
                                r, e = RipFunCall.wrap_fun(the_fun)
                            if fun_key in seen_functions.keys():
                                seen_functions[fun_key] += 1
                            else:
                                seen_functions[fun_key] = 0
                            fun_name = str(fun_key) + "!" + str(seen_functions[fun_key])
                            res[fun_name] = {
                                "call": fun_key,
                                "id": seen_functions[fun_key],
                                "result": r,
                                "errors": str(e),
                                "args": str(fun_args_wargs),
                                "client_call_array_id": i
                            }
                        else:
                            res["err_elem_" + str(i)] = "null function key"
                    else:
                        res["err_elem_" + str(i)] = "null function"
                except Exception as exc:
                    res["err_elem_" + str(i)] = traceback.print_exception(type(exc), exc, exc.__traceback__)
                    # for ex in exc:
                    #     res["err_elem_" + str(i)] += res["err_elem_" + str(i)] \
                    #                                  + " | " + traceback.print_exception(type(ex),
                    #                                                                      exc,
                    #                                                                      exc.__traceback__)
                    # res["err_elem_" + str(i)] = str(exc) + " track " + str(exc.with_traceback())
                i += 1
        return res
