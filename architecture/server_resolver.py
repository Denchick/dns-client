import sys

if sys.platform == 'win32':
    try:
        import winreg as _winreg
    except ImportError:
        import _winreg  # pylint: disable=import-error

def read_registry(self):
    """Extract resolver configuration from the Windows registry."""

    lm = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    want_scan = False
    try:
        try:
            # XP, 2000
            tcp_params = _winreg.OpenKey(lm,
                                         r'SYSTEM\CurrentControlSet'
                                         r'\Services\Tcpip\Parameters')
            want_scan = True
        except EnvironmentError:
            # ME
            tcp_params = _winreg.OpenKey(lm,
                                         r'SYSTEM\CurrentControlSet'
                                         r'\Services\VxD\MSTCP')
        try:
            self._config_win32_fromkey(tcp_params, True)
        finally:
            tcp_params.Close()
        if want_scan:
            interfaces = _winreg.OpenKey(lm,
                                         r'SYSTEM\CurrentControlSet'
                                         r'\Services\Tcpip\Parameters'
                                         r'\Interfaces')
            try:
                i = 0
                while True:
                    try:
                        guid = _winreg.EnumKey(interfaces, i)
                        i += 1
                        key = _winreg.OpenKey(interfaces, guid)
                        if not self._win32_is_nic_enabled(lm, guid, key):
                            continue
                        try:
                            self._config_win32_fromkey(key, False)
                        finally:
                            key.Close()
                    except EnvironmentError:
                        break
            finally:
                interfaces.Close()
    finally:
        lm.Close()


def _win32_is_nic_enabled(self, lm, guid, interface_key):
    # Look in the Windows Registry to determine whether the network
    # interface corresponding to the given guid is enabled.
    #
    # (Code contributed by Paul Marks, thanks!)
    #
    try:
        # This hard-coded location seems to be consistent, at least
        # from Windows 2000 through Vista.
        connection_key = _winreg.OpenKey(
            lm,
            r'SYSTEM\CurrentControlSet\Control\Network'
            r'\{4D36E972-E325-11CE-BFC1-08002BE10318}'
            r'\%s\Connection' % guid)

        try:
            # The PnpInstanceID points to a key inside Enum
            (pnp_id, ttype) = _winreg.QueryValueEx(
                connection_key, 'PnpInstanceID')

            if ttype != _winreg.REG_SZ:
                raise ValueError

            device_key = _winreg.OpenKey(
                lm, r'SYSTEM\CurrentControlSet\Enum\%s' % pnp_id)

            try:
                # Get ConfigFlags for this device
                (flags, ttype) = _winreg.QueryValueEx(
                    device_key, 'ConfigFlags')

                if ttype != _winreg.REG_DWORD:
                    raise ValueError

                # Based on experimentation, bit 0x1 indicates that the
                # device is disabled.
                return not flags & 0x1

            finally:
                device_key.Close()
        finally:
            connection_key.Close()
    except (EnvironmentError, ValueError):
        # Pre-vista, enabled interfaces seem to have a non-empty
        # NTEContextList; this was how dnspython detected enabled
        # nics before the code above was contributed.  We've retained
        # the old method since we don't know if the code above works
        # on Windows 95/98/ME.
        try:
            (nte, ttype) = _winreg.QueryValueEx(interface_key,
                                                'NTEContextList')
            return nte is not None
        except WindowsError:  # pylint: disable=undefined-variable
            return False