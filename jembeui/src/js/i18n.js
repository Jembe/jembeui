function setJembeuiTimezoneCookie(timezone) {
    if (timezone !== undefined && timezone !== null) {
        document.cookie = `jembeuiTimezone=${timezone};`
    } else {
        const timezoneCookie = document.cookie.split('; ').find(
            item => item.trim().startsWith('jembeuiTimezone=')
        )
        const currentTimezone = timezoneCookie !== undefined ? timezoneCookie.trim().split('=')[1] : null;
        timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (currentTimezone !== timezone) {
            document.cookie = `jembeuiTimezone=${timezone};`
        }
    }
}
function setJembeuiLocaleCookie(localeCode) {
    if (localeCode !== undefined && localeCode !== null) {
        document.cookie = `jembeuiLocaleCode=${localeCode};`
    }
}

setJembeuiTimezoneCookie();