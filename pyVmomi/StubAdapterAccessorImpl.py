# **********************************************************
# Copyright (c) 2011-2023 VMware, Inc.
# **********************************************************

from .VmomiSupport import GetVmodlType, ManagedObject, Object


# Used to replace few type definitions for emulating
# legacy behavior. Ref. VmomiSupport._wsdlTypeMap
_legacyTypes = {
    "type": "string",
    "ManagedMethod": "string",
    "PropertyPath": "string",
    "type[]": "string[]",
    "ManagedMethod[]": "string[]",
    "PropertyPath[]": "string[]"
}


class StubAdapterAccessorMixin:

    # Retrieve a managed property
    #
    # @param self self
    # @param mo managed object
    # @param info property info
    def InvokeAccessor(self, mo, info):
        prop = info.name
        param = Object(name="prop", type=str, version=self.version, flags=0)

        # Emulate legacy behavior for backward compatibility
        replacement = _legacyTypes.get(info.type.__name__, None)
        if replacement:
            info.type = GetVmodlType(replacement)

        info = Object(name=info.name,
                      type=ManagedObject,
                      wsdlName="Fetch",
                      version=info.version,
                      params=(param, ),
                      isTask=False,
                      resultFlags=info.flags,
                      result=info.type,
                      methodResult=info.type)
        return self.InvokeMethod(mo, info, (prop, ))

    def SupportServerGUIDs(self):
        return False
