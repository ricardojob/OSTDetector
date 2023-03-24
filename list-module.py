import sys as os
# Printing different functions in sys module
print(len(dir(os)))


# # Importing getmembers and isfunction from inspect
# from inspect import getmembers, isfunction
# import types

# # Importing math module
# import sys as sos
# # Printing all the functions in math module
# # [print(a) for a in getmembers(sos,isfunction)] #, )
# # print([getattr(sys, a) for a in dir(sys)
# #   if isinstance(getattr(sys, a), types.FunctionType)])

# print(a for a in getmembers(sos) if isfunction(a[1]))  