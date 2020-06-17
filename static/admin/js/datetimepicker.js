//! moment.js
//! version : 2.14.1
//! authors : Tim Wood, Iskren Chernev, Moment.js contributors
//! license : MIT
//! momentjs.com
! function(a, b) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = b() : "function" == typeof define && define.amd ? define(b) : a.moment = b()
}(this, function() {
    "use strict";

    function a() {
        return md.apply(null, arguments)
    }
    // This is done to register the method called with moment()
    // without creating circular dependencies.
    function b(a) {
        md = a
    }

    function c(a) {
        return a instanceof Array || "[object Array]" === Object.prototype.toString.call(a)
    }

    function d(a) {
        return "[object Object]" === Object.prototype.toString.call(a)
    }

    function e(a) {
        var b;
        for (b in a)
            // even if its not own property I'd still call it non-empty
            return !1;
        return !0
    }

    function f(a) {
        return a instanceof Date || "[object Date]" === Object.prototype.toString.call(a)
    }

    function g(a, b) {
        var c, d = [];
        for (c = 0; c < a.length; ++c) d.push(b(a[c], c));
        return d
    }

    function h(a, b) {
        return Object.prototype.hasOwnProperty.call(a, b)
    }

    function i(a, b) {
        for (var c in b) h(b, c) && (a[c] = b[c]);
        return h(b, "toString") && (a.toString = b.toString), h(b, "valueOf") && (a.valueOf = b.valueOf), a
    }

    function j(a, b, c, d) {
        return qb(a, b, c, d, !0).utc()
    }

    function k() {
        // We need to deep clone this object.
        return {
            empty: !1,
            unusedTokens: [],
            unusedInput: [],
            overflow: -2,
            charsLeftOver: 0,
            nullInput: !1,
            invalidMonth: null,
            invalidFormat: !1,
            userInvalidated: !1,
            iso: !1,
            parsedDateParts: [],
            meridiem: null
        }
    }

    function l(a) {
        return null == a._pf && (a._pf = k()), a._pf
    }

    function m(a) {
        if (null == a._isValid) {
            var b = l(a),
                c = nd.call(b.parsedDateParts, function(a) {
                    return null != a
                });
            a._isValid = !isNaN(a._d.getTime()) && b.overflow < 0 && !b.empty && !b.invalidMonth && !b.invalidWeekday && !b.nullInput && !b.invalidFormat && !b.userInvalidated && (!b.meridiem || b.meridiem && c), a._strict && (a._isValid = a._isValid && 0 === b.charsLeftOver && 0 === b.unusedTokens.length && void 0 === b.bigHour)
        }
        return a._isValid
    }

    function n(a) {
        var b = j(NaN);
        return null != a ? i(l(b), a) : l(b).userInvalidated = !0, b
    }

    function o(a) {
        return void 0 === a
    }

    function p(a, b) {
        var c, d, e;
        if (o(b._isAMomentObject) || (a._isAMomentObject = b._isAMomentObject), o(b._i) || (a._i = b._i), o(b._f) || (a._f = b._f), o(b._l) || (a._l = b._l), o(b._strict) || (a._strict = b._strict), o(b._tzm) || (a._tzm = b._tzm), o(b._isUTC) || (a._isUTC = b._isUTC), o(b._offset) || (a._offset = b._offset), o(b._pf) || (a._pf = l(b)), o(b._locale) || (a._locale = b._locale), od.length > 0)
            for (c in od) d = od[c], e = b[d], o(e) || (a[d] = e);
        return a
    }
    // Moment prototype object
    function q(b) {
        p(this, b), this._d = new Date(null != b._d ? b._d.getTime() : NaN), pd === !1 && (pd = !0, a.updateOffset(this), pd = !1)
    }

    function r(a) {
        return a instanceof q || null != a && null != a._isAMomentObject
    }

    function s(a) {
        return 0 > a ? Math.ceil(a) || 0 : Math.floor(a)
    }

    function t(a) {
        var b = +a,
            c = 0;
        return 0 !== b && isFinite(b) && (c = s(b)), c
    }
    // compare two arrays, return the number of differences
    function u(a, b, c) {
        var d, e = Math.min(a.length, b.length),
            f = Math.abs(a.length - b.length),
            g = 0;
        for (d = 0; e > d; d++)(c && a[d] !== b[d] || !c && t(a[d]) !== t(b[d])) && g++;
        return g + f
    }

    function v(b) {
        a.suppressDeprecationWarnings === !1 && "undefined" != typeof console && console.warn && console.warn("Deprecation warning: " + b)
    }

    function w(b, c) {
        var d = !0;
        return i(function() {
            return null != a.deprecationHandler && a.deprecationHandler(null, b), d && (v(b + "\nArguments: " + Array.prototype.slice.call(arguments).join(", ") + "\n" + (new Error).stack), d = !1), c.apply(this, arguments)
        }, c)
    }

    function x(b, c) {
        null != a.deprecationHandler && a.deprecationHandler(b, c), qd[b] || (v(c), qd[b] = !0)
    }

    function y(a) {
        return a instanceof Function || "[object Function]" === Object.prototype.toString.call(a)
    }

    function z(a) {
        var b, c;
        for (c in a) b = a[c], y(b) ? this[c] = b : this["_" + c] = b;
        this._config = a,
            // Lenient ordinal parsing accepts just a number in addition to
            // number + (possibly) stuff coming from _ordinalParseLenient.
            this._ordinalParseLenient = new RegExp(this._ordinalParse.source + "|" + /\d{1,2}/.source)
    }

    function A(a, b) {
        var c, e = i({}, a);
        for (c in b) h(b, c) && (d(a[c]) && d(b[c]) ? (e[c] = {}, i(e[c], a[c]), i(e[c], b[c])) : null != b[c] ? e[c] = b[c] : delete e[c]);
        for (c in a) h(a, c) && !h(b, c) && d(a[c]) && (
            // make sure changes to properties don't modify parent config
            e[c] = i({}, e[c]));
        return e
    }

    function B(a) {
        null != a && this.set(a)
    }

    function C(a, b, c) {
        var d = this._calendar[a] || this._calendar.sameElse;
        return y(d) ? d.call(b, c) : d
    }

    function D(a) {
        var b = this._longDateFormat[a],
            c = this._longDateFormat[a.toUpperCase()];
        return b || !c ? b : (this._longDateFormat[a] = c.replace(/MMMM|MM|DD|dddd/g, function(a) {
            return a.slice(1)
        }), this._longDateFormat[a])
    }

    function E() {
        return this._invalidDate
    }

    function F(a) {
        return this._ordinal.replace("%d", a)
    }

    function G(a, b, c, d) {
        var e = this._relativeTime[c];
        return y(e) ? e(a, b, c, d) : e.replace(/%d/i, a)
    }

    function H(a, b) {
        var c = this._relativeTime[a > 0 ? "future" : "past"];
        return y(c) ? c(b) : c.replace(/%s/i, b)
    }

    function I(a, b) {
        var c = a.toLowerCase();
        zd[c] = zd[c + "s"] = zd[b] = a
    }

    function J(a) {
        return "string" == typeof a ? zd[a] || zd[a.toLowerCase()] : void 0
    }

    function K(a) {
        var b, c, d = {};
        for (c in a) h(a, c) && (b = J(c), b && (d[b] = a[c]));
        return d
    }

    function L(a, b) {
        Ad[a] = b
    }

    function M(a) {
        var b = [];
        for (var c in a) b.push({
            unit: c,
            priority: Ad[c]
        });
        return b.sort(function(a, b) {
            return a.priority - b.priority
        }), b
    }

    function N(b, c) {
        return function(d) {
            return null != d ? (P(this, b, d), a.updateOffset(this, c), this) : O(this, b)
        }
    }

    function O(a, b) {
        return a.isValid() ? a._d["get" + (a._isUTC ? "UTC" : "") + b]() : NaN
    }

    function P(a, b, c) {
        a.isValid() && a._d["set" + (a._isUTC ? "UTC" : "") + b](c)
    }
    // MOMENTS
    function Q(a) {
        return a = J(a), y(this[a]) ? this[a]() : this
    }

    function R(a, b) {
        if ("object" == typeof a) {
            a = K(a);
            for (var c = M(a), d = 0; d < c.length; d++) this[c[d].unit](a[c[d].unit])
        } else if (a = J(a), y(this[a])) return this[a](b);
        return this
    }

    function S(a, b, c) {
        var d = "" + Math.abs(a),
            e = b - d.length,
            f = a >= 0;
        return (f ? c ? "+" : "" : "-") + Math.pow(10, Math.max(0, e)).toString().substr(1) + d
    }
    // token:    'M'
    // padded:   ['MM', 2]
    // ordinal:  'Mo'
    // callback: function () { this.month() + 1 }
    function T(a, b, c, d) {
        var e = d;
        "string" == typeof d && (e = function() {
            return this[d]()
        }), a && (Ed[a] = e), b && (Ed[b[0]] = function() {
            return S(e.apply(this, arguments), b[1], b[2])
        }), c && (Ed[c] = function() {
            return this.localeData().ordinal(e.apply(this, arguments), a)
        })
    }

    function U(a) {
        return a.match(/\[[\s\S]/) ? a.replace(/^\[|\]$/g, "") : a.replace(/\\/g, "")
    }

    function V(a) {
        var b, c, d = a.match(Bd);
        for (b = 0, c = d.length; c > b; b++) Ed[d[b]] ? d[b] = Ed[d[b]] : d[b] = U(d[b]);
        return function(b) {
            var e, f = "";
            for (e = 0; c > e; e++) f += d[e] instanceof Function ? d[e].call(b, a) : d[e];
            return f
        }
    }
    // format date using native date object
    function W(a, b) {
        return a.isValid() ? (b = X(b, a.localeData()), Dd[b] = Dd[b] || V(b), Dd[b](a)) : a.localeData().invalidDate()
    }

    function X(a, b) {
        function c(a) {
            return b.longDateFormat(a) || a
        }
        var d = 5;
        for (Cd.lastIndex = 0; d >= 0 && Cd.test(a);) a = a.replace(Cd, c), Cd.lastIndex = 0, d -= 1;
        return a
    }

    function Y(a, b, c) {
        Wd[a] = y(b) ? b : function(a, d) {
            return a && c ? c : b
        }
    }

    function Z(a, b) {
        return h(Wd, a) ? Wd[a](b._strict, b._locale) : new RegExp($(a))
    }
    // Code from http://stackoverflow.com/questions/3561493/is-there-a-regexp-escape-function-in-javascript
    function $(a) {
        return _(a.replace("\\", "").replace(/\\(\[)|\\(\])|\[([^\]\[]*)\]|\\(.)/g, function(a, b, c, d, e) {
            return b || c || d || e
        }))
    }

    function _(a) {
        return a.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&")
    }

    function aa(a, b) {
        var c, d = b;
        for ("string" == typeof a && (a = [a]), "number" == typeof b && (d = function(a, c) {
                c[b] = t(a)
            }), c = 0; c < a.length; c++) Xd[a[c]] = d
    }

    function ba(a, b) {
        aa(a, function(a, c, d, e) {
            d._w = d._w || {}, b(a, d._w, d, e)
        })
    }

    function ca(a, b, c) {
        null != b && h(Xd, a) && Xd[a](b, c._a, c, a)
    }

    function da(a, b) {
        return new Date(Date.UTC(a, b + 1, 0)).getUTCDate()
    }

    function ea(a, b) {
        return c(this._months) ? this._months[a.month()] : this._months[(this._months.isFormat || fe).test(b) ? "format" : "standalone"][a.month()]
    }

    function fa(a, b) {
        return c(this._monthsShort) ? this._monthsShort[a.month()] : this._monthsShort[fe.test(b) ? "format" : "standalone"][a.month()]
    }

    function ga(a, b, c) {
        var d, e, f, g = a.toLocaleLowerCase();
        if (!this._monthsParse)
            for (
                // this is not used
                this._monthsParse = [], this._longMonthsParse = [], this._shortMonthsParse = [], d = 0; 12 > d; ++d) f = j([2e3, d]), this._shortMonthsParse[d] = this.monthsShort(f, "").toLocaleLowerCase(), this._longMonthsParse[d] = this.months(f, "").toLocaleLowerCase();
        return c ? "MMM" === b ? (e = sd.call(this._shortMonthsParse, g), -1 !== e ? e : null) : (e = sd.call(this._longMonthsParse, g), -1 !== e ? e : null) : "MMM" === b ? (e = sd.call(this._shortMonthsParse, g), -1 !== e ? e : (e = sd.call(this._longMonthsParse, g), -1 !== e ? e : null)) : (e = sd.call(this._longMonthsParse, g), -1 !== e ? e : (e = sd.call(this._shortMonthsParse, g), -1 !== e ? e : null))
    }

    function ha(a, b, c) {
        var d, e, f;
        if (this._monthsParseExact) return ga.call(this, a, b, c);
        // TODO: add sorting
        // Sorting makes sure if one month (or abbr) is a prefix of another
        // see sorting in computeMonthsParse
        for (this._monthsParse || (this._monthsParse = [], this._longMonthsParse = [], this._shortMonthsParse = []), d = 0; 12 > d; d++) {
            // test the regex
            if (e = j([2e3, d]), c && !this._longMonthsParse[d] && (this._longMonthsParse[d] = new RegExp("^" + this.months(e, "").replace(".", "") + "$", "i"), this._shortMonthsParse[d] = new RegExp("^" + this.monthsShort(e, "").replace(".", "") + "$", "i")), c || this._monthsParse[d] || (f = "^" + this.months(e, "") + "|^" + this.monthsShort(e, ""), this._monthsParse[d] = new RegExp(f.replace(".", ""), "i")), c && "MMMM" === b && this._longMonthsParse[d].test(a)) return d;
            if (c && "MMM" === b && this._shortMonthsParse[d].test(a)) return d;
            if (!c && this._monthsParse[d].test(a)) return d
        }
    }
    // MOMENTS
    function ia(a, b) {
        var c;
        if (!a.isValid())
            // No op
            return a;
        if ("string" == typeof b)
            if (/^\d+$/.test(b)) b = t(b);
            else
                // TODO: Another silent failure?
                if (b = a.localeData().monthsParse(b), "number" != typeof b) return a;
        return c = Math.min(a.date(), da(a.year(), b)), a._d["set" + (a._isUTC ? "UTC" : "") + "Month"](b, c), a
    }

    function ja(b) {
        return null != b ? (ia(this, b), a.updateOffset(this, !0), this) : O(this, "Month")
    }

    function ka() {
        return da(this.year(), this.month())
    }

    function la(a) {
        return this._monthsParseExact ? (h(this, "_monthsRegex") || na.call(this), a ? this._monthsShortStrictRegex : this._monthsShortRegex) : (h(this, "_monthsShortRegex") || (this._monthsShortRegex = ie), this._monthsShortStrictRegex && a ? this._monthsShortStrictRegex : this._monthsShortRegex)
    }

    function ma(a) {
        return this._monthsParseExact ? (h(this, "_monthsRegex") || na.call(this), a ? this._monthsStrictRegex : this._monthsRegex) : (h(this, "_monthsRegex") || (this._monthsRegex = je), this._monthsStrictRegex && a ? this._monthsStrictRegex : this._monthsRegex)
    }

    function na() {
        function a(a, b) {
            return b.length - a.length
        }
        var b, c, d = [],
            e = [],
            f = [];
        for (b = 0; 12 > b; b++) c = j([2e3, b]), d.push(this.monthsShort(c, "")), e.push(this.months(c, "")), f.push(this.months(c, "")), f.push(this.monthsShort(c, ""));
        for (
            // Sorting makes sure if one month (or abbr) is a prefix of another it
            // will match the longer piece.
            d.sort(a), e.sort(a), f.sort(a), b = 0; 12 > b; b++) d[b] = _(d[b]), e[b] = _(e[b]);
        for (b = 0; 24 > b; b++) f[b] = _(f[b]);
        this._monthsRegex = new RegExp("^(" + f.join("|") + ")", "i"), this._monthsShortRegex = this._monthsRegex, this._monthsStrictRegex = new RegExp("^(" + e.join("|") + ")", "i"), this._monthsShortStrictRegex = new RegExp("^(" + d.join("|") + ")", "i")
    }
    // HELPERS
    function oa(a) {
        return pa(a) ? 366 : 365
    }

    function pa(a) {
        return a % 4 === 0 && a % 100 !== 0 || a % 400 === 0
    }

    function qa() {
        return pa(this.year())
    }

    function ra(a, b, c, d, e, f, g) {
        //can't just apply() to create a date:
        //http://stackoverflow.com/questions/181348/instantiating-a-javascript-object-by-calling-prototype-constructor-apply
        var h = new Date(a, b, c, d, e, f, g);
        //the date constructor remaps years 0-99 to 1900-1999
        return 100 > a && a >= 0 && isFinite(h.getFullYear()) && h.setFullYear(a), h
    }

    function sa(a) {
        var b = new Date(Date.UTC.apply(null, arguments));
        //the Date.UTC function remaps years 0-99 to 1900-1999
        return 100 > a && a >= 0 && isFinite(b.getUTCFullYear()) && b.setUTCFullYear(a), b
    }
    // start-of-first-week - start-of-year
    function ta(a, b, c) {
        var // first-week day -- which january is always in the first week (4 for iso, 1 for other)
            d = 7 + b - c,
            // first-week day local weekday -- which local weekday is fwd
            e = (7 + sa(a, 0, d).getUTCDay() - b) % 7;
        return -e + d - 1
    }
    //http://en.wikipedia.org/wiki/ISO_week_date#Calculating_a_date_given_the_year.2C_week_number_and_weekday
    function ua(a, b, c, d, e) {
        var f, g, h = (7 + c - d) % 7,
            i = ta(a, d, e),
            j = 1 + 7 * (b - 1) + h + i;
        return 0 >= j ? (f = a - 1, g = oa(f) + j) : j > oa(a) ? (f = a + 1, g = j - oa(a)) : (f = a, g = j), {
            year: f,
            dayOfYear: g
        }
    }

    function va(a, b, c) {
        var d, e, f = ta(a.year(), b, c),
            g = Math.floor((a.dayOfYear() - f - 1) / 7) + 1;
        return 1 > g ? (e = a.year() - 1, d = g + wa(e, b, c)) : g > wa(a.year(), b, c) ? (d = g - wa(a.year(), b, c), e = a.year() + 1) : (e = a.year(), d = g), {
            week: d,
            year: e
        }
    }

    function wa(a, b, c) {
        var d = ta(a, b, c),
            e = ta(a + 1, b, c);
        return (oa(a) - d + e) / 7
    }
    // HELPERS
    // LOCALES
    function xa(a) {
        return va(a, this._week.dow, this._week.doy).week
    }

    function ya() {
        return this._week.dow
    }

    function za() {
        return this._week.doy
    }
    // MOMENTS
    function Aa(a) {
        var b = this.localeData().week(this);
        return null == a ? b : this.add(7 * (a - b), "d")
    }

    function Ba(a) {
        var b = va(this, 1, 4).week;
        return null == a ? b : this.add(7 * (a - b), "d")
    }
    // HELPERS
    function Ca(a, b) {
        return "string" != typeof a ? a : isNaN(a) ? (a = b.weekdaysParse(a), "number" == typeof a ? a : null) : parseInt(a, 10)
    }

    function Da(a, b) {
        return "string" == typeof a ? b.weekdaysParse(a) % 7 || 7 : isNaN(a) ? null : a
    }

    function Ea(a, b) {
        return c(this._weekdays) ? this._weekdays[a.day()] : this._weekdays[this._weekdays.isFormat.test(b) ? "format" : "standalone"][a.day()]
    }

    function Fa(a) {
        return this._weekdaysShort[a.day()]
    }

    function Ga(a) {
        return this._weekdaysMin[a.day()]
    }

    function Ha(a, b, c) {
        var d, e, f, g = a.toLocaleLowerCase();
        if (!this._weekdaysParse)
            for (this._weekdaysParse = [], this._shortWeekdaysParse = [], this._minWeekdaysParse = [], d = 0; 7 > d; ++d) f = j([2e3, 1]).day(d), this._minWeekdaysParse[d] = this.weekdaysMin(f, "").toLocaleLowerCase(), this._shortWeekdaysParse[d] = this.weekdaysShort(f, "").toLocaleLowerCase(), this._weekdaysParse[d] = this.weekdays(f, "").toLocaleLowerCase();
        return c ? "dddd" === b ? (e = sd.call(this._weekdaysParse, g), -1 !== e ? e : null) : "ddd" === b ? (e = sd.call(this._shortWeekdaysParse, g), -1 !== e ? e : null) : (e = sd.call(this._minWeekdaysParse, g), -1 !== e ? e : null) : "dddd" === b ? (e = sd.call(this._weekdaysParse, g), -1 !== e ? e : (e = sd.call(this._shortWeekdaysParse, g), -1 !== e ? e : (e = sd.call(this._minWeekdaysParse, g), -1 !== e ? e : null))) : "ddd" === b ? (e = sd.call(this._shortWeekdaysParse, g), -1 !== e ? e : (e = sd.call(this._weekdaysParse, g), -1 !== e ? e : (e = sd.call(this._minWeekdaysParse, g), -1 !== e ? e : null))) : (e = sd.call(this._minWeekdaysParse, g), -1 !== e ? e : (e = sd.call(this._weekdaysParse, g), -1 !== e ? e : (e = sd.call(this._shortWeekdaysParse, g), -1 !== e ? e : null)))
    }

    function Ia(a, b, c) {
        var d, e, f;
        if (this._weekdaysParseExact) return Ha.call(this, a, b, c);
        for (this._weekdaysParse || (this._weekdaysParse = [], this._minWeekdaysParse = [], this._shortWeekdaysParse = [], this._fullWeekdaysParse = []), d = 0; 7 > d; d++) {
            // test the regex
            if (e = j([2e3, 1]).day(d), c && !this._fullWeekdaysParse[d] && (this._fullWeekdaysParse[d] = new RegExp("^" + this.weekdays(e, "").replace(".", ".?") + "$", "i"), this._shortWeekdaysParse[d] = new RegExp("^" + this.weekdaysShort(e, "").replace(".", ".?") + "$", "i"), this._minWeekdaysParse[d] = new RegExp("^" + this.weekdaysMin(e, "").replace(".", ".?") + "$", "i")), this._weekdaysParse[d] || (f = "^" + this.weekdays(e, "") + "|^" + this.weekdaysShort(e, "") + "|^" + this.weekdaysMin(e, ""), this._weekdaysParse[d] = new RegExp(f.replace(".", ""), "i")), c && "dddd" === b && this._fullWeekdaysParse[d].test(a)) return d;
            if (c && "ddd" === b && this._shortWeekdaysParse[d].test(a)) return d;
            if (c && "dd" === b && this._minWeekdaysParse[d].test(a)) return d;
            if (!c && this._weekdaysParse[d].test(a)) return d
        }
    }
    // MOMENTS
    function Ja(a) {
        if (!this.isValid()) return null != a ? this : NaN;
        var b = this._isUTC ? this._d.getUTCDay() : this._d.getDay();
        return null != a ? (a = Ca(a, this.localeData()), this.add(a - b, "d")) : b
    }

    function Ka(a) {
        if (!this.isValid()) return null != a ? this : NaN;
        var b = (this.day() + 7 - this.localeData()._week.dow) % 7;
        return null == a ? b : this.add(a - b, "d")
    }

    function La(a) {
        if (!this.isValid()) return null != a ? this : NaN;
        // behaves the same as moment#day except
        // as a getter, returns 7 instead of 0 (1-7 range instead of 0-6)
        // as a setter, sunday should belong to the previous week.
        if (null != a) {
            var b = Da(a, this.localeData());
            return this.day(this.day() % 7 ? b : b - 7)
        }
        return this.day() || 7
    }

    function Ma(a) {
        return this._weekdaysParseExact ? (h(this, "_weekdaysRegex") || Pa.call(this), a ? this._weekdaysStrictRegex : this._weekdaysRegex) : (h(this, "_weekdaysRegex") || (this._weekdaysRegex = pe), this._weekdaysStrictRegex && a ? this._weekdaysStrictRegex : this._weekdaysRegex)
    }

    function Na(a) {
        return this._weekdaysParseExact ? (h(this, "_weekdaysRegex") || Pa.call(this), a ? this._weekdaysShortStrictRegex : this._weekdaysShortRegex) : (h(this, "_weekdaysShortRegex") || (this._weekdaysShortRegex = qe), this._weekdaysShortStrictRegex && a ? this._weekdaysShortStrictRegex : this._weekdaysShortRegex)
    }

    function Oa(a) {
        return this._weekdaysParseExact ? (h(this, "_weekdaysRegex") || Pa.call(this), a ? this._weekdaysMinStrictRegex : this._weekdaysMinRegex) : (h(this, "_weekdaysMinRegex") || (this._weekdaysMinRegex = re), this._weekdaysMinStrictRegex && a ? this._weekdaysMinStrictRegex : this._weekdaysMinRegex)
    }

    function Pa() {
        function a(a, b) {
            return b.length - a.length
        }
        var b, c, d, e, f, g = [],
            h = [],
            i = [],
            k = [];
        for (b = 0; 7 > b; b++) c = j([2e3, 1]).day(b), d = this.weekdaysMin(c, ""), e = this.weekdaysShort(c, ""), f = this.weekdays(c, ""), g.push(d), h.push(e), i.push(f), k.push(d), k.push(e), k.push(f);
        for (
            // Sorting makes sure if one weekday (or abbr) is a prefix of another it
            // will match the longer piece.
            g.sort(a), h.sort(a), i.sort(a), k.sort(a), b = 0; 7 > b; b++) h[b] = _(h[b]), i[b] = _(i[b]), k[b] = _(k[b]);
        this._weekdaysRegex = new RegExp("^(" + k.join("|") + ")", "i"), this._weekdaysShortRegex = this._weekdaysRegex, this._weekdaysMinRegex = this._weekdaysRegex, this._weekdaysStrictRegex = new RegExp("^(" + i.join("|") + ")", "i"), this._weekdaysShortStrictRegex = new RegExp("^(" + h.join("|") + ")", "i"), this._weekdaysMinStrictRegex = new RegExp("^(" + g.join("|") + ")", "i")
    }
    // FORMATTING
    function Qa() {
        return this.hours() % 12 || 12
    }

    function Ra() {
        return this.hours() || 24
    }

    function Sa(a, b) {
        T(a, 0, 0, function() {
            return this.localeData().meridiem(this.hours(), this.minutes(), b)
        })
    }
    // PARSING
    function Ta(a, b) {
        return b._meridiemParse
    }
    // LOCALES
    function Ua(a) {
        // IE8 Quirks Mode & IE7 Standards Mode do not allow accessing strings like arrays
        // Using charAt should be more compatible.
        return "p" === (a + "").toLowerCase().charAt(0)
    }

    function Va(a, b, c) {
        return a > 11 ? c ? "pm" : "PM" : c ? "am" : "AM"
    }

    function Wa(a) {
        return a ? a.toLowerCase().replace("_", "-") : a
    }
    // pick the locale from the array
    // try ['en-au', 'en-gb'] as 'en-au', 'en-gb', 'en', as in move through the list trying each
    // substring from most specific to least, but move to the next array item if it's a more specific variant than the current root
    function Xa(a) {
        for (var b, c, d, e, f = 0; f < a.length;) {
            for (e = Wa(a[f]).split("-"), b = e.length, c = Wa(a[f + 1]), c = c ? c.split("-") : null; b > 0;) {
                if (d = Ya(e.slice(0, b).join("-"))) return d;
                if (c && c.length >= b && u(e, c, !0) >= b - 1)
                    //the next array item is better than a shallower substring of this one
                    break;
                b--
            }
            f++
        }
        return null
    }

    function Ya(a) {
        var b = null;
        // TODO: Find a better way to register and load all the locales in Node
        if (!we[a] && "undefined" != typeof module && module && module.exports) try {
            b = se._abbr, require("./locale/" + a),
                // because defineLocale currently also sets the global locale, we
                // want to undo that for lazy loaded locales
                Za(b)
        } catch (c) {}
        return we[a]
    }
    // This function will load locale and then set the global locale.  If
    // no arguments are passed in, it will simply return the current global
    // locale key.
    function Za(a, b) {
        var c;
        // moment.duration._locale = moment._locale = data;
        return a && (c = o(b) ? ab(a) : $a(a, b), c && (se = c)), se._abbr
    }

    function $a(a, b) {
        if (null !== b) {
            var c = ve;
            // treat as if there is no base config
            // backwards compat for now: also set the locale
            return b.abbr = a, null != we[a] ? (x("defineLocaleOverride", "use moment.updateLocale(localeName, config) to change an existing locale. moment.defineLocale(localeName, config) should only be used for creating a new locale See http://momentjs.com/guides/#/warnings/define-locale/ for more info."), c = we[a]._config) : null != b.parentLocale && (null != we[b.parentLocale] ? c = we[b.parentLocale]._config : x("parentLocaleUndefined", "specified parentLocale is not defined yet. See http://momentjs.com/guides/#/warnings/parent-locale/")), we[a] = new B(A(c, b)), Za(a), we[a]
        }
        // useful for testing
        return delete we[a], null
    }

    function _a(a, b) {
        if (null != b) {
            var c, d = ve;
            // MERGE
            null != we[a] && (d = we[a]._config), b = A(d, b), c = new B(b), c.parentLocale = we[a], we[a] = c,
                // backwards compat for now: also set the locale
                Za(a)
        } else
            // pass null for config to unupdate, useful for tests
            null != we[a] && (null != we[a].parentLocale ? we[a] = we[a].parentLocale : null != we[a] && delete we[a]);
        return we[a]
    }
    // returns locale data
    function ab(a) {
        var b;
        if (a && a._locale && a._locale._abbr && (a = a._locale._abbr), !a) return se;
        if (!c(a)) {
            if (b = Ya(a)) return b;
            a = [a]
        }
        return Xa(a)
    }

    function bb() {
        return rd(we)
    }

    function cb(a) {
        var b, c = a._a;
        return c && -2 === l(a).overflow && (b = c[Zd] < 0 || c[Zd] > 11 ? Zd : c[$d] < 1 || c[$d] > da(c[Yd], c[Zd]) ? $d : c[_d] < 0 || c[_d] > 24 || 24 === c[_d] && (0 !== c[ae] || 0 !== c[be] || 0 !== c[ce]) ? _d : c[ae] < 0 || c[ae] > 59 ? ae : c[be] < 0 || c[be] > 59 ? be : c[ce] < 0 || c[ce] > 999 ? ce : -1, l(a)._overflowDayOfYear && (Yd > b || b > $d) && (b = $d), l(a)._overflowWeeks && -1 === b && (b = de), l(a)._overflowWeekday && -1 === b && (b = ee), l(a).overflow = b), a
    }
    // date from iso format
    function db(a) {
        var b, c, d, e, f, g, h = a._i,
            i = xe.exec(h) || ye.exec(h);
        if (i) {
            for (l(a).iso = !0, b = 0, c = Ae.length; c > b; b++)
                if (Ae[b][1].exec(i[1])) {
                    e = Ae[b][0], d = Ae[b][2] !== !1;
                    break
                }
            if (null == e) return void(a._isValid = !1);
            if (i[3]) {
                for (b = 0, c = Be.length; c > b; b++)
                    if (Be[b][1].exec(i[3])) {
                        // match[2] should be 'T' or space
                        f = (i[2] || " ") + Be[b][0];
                        break
                    }
                if (null == f) return void(a._isValid = !1)
            }
            if (!d && null != f) return void(a._isValid = !1);
            if (i[4]) {
                if (!ze.exec(i[4])) return void(a._isValid = !1);
                g = "Z"
            }
            a._f = e + (f || "") + (g || ""), jb(a)
        } else a._isValid = !1
    }
    // date from iso format or fallback
    function eb(b) {
        var c = Ce.exec(b._i);
        return null !== c ? void(b._d = new Date(+c[1])) : (db(b), void(b._isValid === !1 && (delete b._isValid, a.createFromInputFallback(b))))
    }
    // Pick the first defined of two or three arguments.
    function fb(a, b, c) {
        return null != a ? a : null != b ? b : c
    }

    function gb(b) {
        // hooks is actually the exported moment object
        var c = new Date(a.now());
        return b._useUTC ? [c.getUTCFullYear(), c.getUTCMonth(), c.getUTCDate()] : [c.getFullYear(), c.getMonth(), c.getDate()]
    }
    // convert an array to a date.
    // the array should mirror the parameters below
    // note: all values past the year are optional and will default to the lowest possible value.
    // [year, month, day , hour, minute, second, millisecond]
    function hb(a) {
        var b, c, d, e, f = [];
        if (!a._d) {
            // Default to current date.
            // * if no year, month, day of month are given, default to today
            // * if day of month is given, default month and year
            // * if month is given, default only year
            // * if year is given, don't default anything
            for (d = gb(a), a._w && null == a._a[$d] && null == a._a[Zd] && ib(a), a._dayOfYear && (e = fb(a._a[Yd], d[Yd]), a._dayOfYear > oa(e) && (l(a)._overflowDayOfYear = !0), c = sa(e, 0, a._dayOfYear), a._a[Zd] = c.getUTCMonth(), a._a[$d] = c.getUTCDate()), b = 0; 3 > b && null == a._a[b]; ++b) a._a[b] = f[b] = d[b];
            // Zero out whatever was not defaulted, including time
            for (; 7 > b; b++) a._a[b] = f[b] = null == a._a[b] ? 2 === b ? 1 : 0 : a._a[b];
            // Check for 24:00:00.000
            24 === a._a[_d] && 0 === a._a[ae] && 0 === a._a[be] && 0 === a._a[ce] && (a._nextDay = !0, a._a[_d] = 0), a._d = (a._useUTC ? sa : ra).apply(null, f),
                // Apply timezone offset from input. The actual utcOffset can be changed
                // with parseZone.
                null != a._tzm && a._d.setUTCMinutes(a._d.getUTCMinutes() - a._tzm), a._nextDay && (a._a[_d] = 24)
        }
    }

    function ib(a) {
        var b, c, d, e, f, g, h, i;
        b = a._w, null != b.GG || null != b.W || null != b.E ? (f = 1, g = 4, c = fb(b.GG, a._a[Yd], va(rb(), 1, 4).year), d = fb(b.W, 1), e = fb(b.E, 1), (1 > e || e > 7) && (i = !0)) : (f = a._locale._week.dow, g = a._locale._week.doy, c = fb(b.gg, a._a[Yd], va(rb(), f, g).year), d = fb(b.w, 1), null != b.d ? (e = b.d, (0 > e || e > 6) && (i = !0)) : null != b.e ? (e = b.e + f, (b.e < 0 || b.e > 6) && (i = !0)) : e = f), 1 > d || d > wa(c, f, g) ? l(a)._overflowWeeks = !0 : null != i ? l(a)._overflowWeekday = !0 : (h = ua(c, d, e, f, g), a._a[Yd] = h.year, a._dayOfYear = h.dayOfYear)
    }
    // date from string and format string
    function jb(b) {
        // TODO: Move this to another part of the creation flow to prevent circular deps
        if (b._f === a.ISO_8601) return void db(b);
        b._a = [], l(b).empty = !0;
        // This array is used to make a Date, either with `new Date` or `Date.UTC`
        var c, d, e, f, g, h = "" + b._i,
            i = h.length,
            j = 0;
        for (e = X(b._f, b._locale).match(Bd) || [], c = 0; c < e.length; c++) f = e[c], d = (h.match(Z(f, b)) || [])[0], d && (g = h.substr(0, h.indexOf(d)), g.length > 0 && l(b).unusedInput.push(g), h = h.slice(h.indexOf(d) + d.length), j += d.length), Ed[f] ? (d ? l(b).empty = !1 : l(b).unusedTokens.push(f), ca(f, d, b)) : b._strict && !d && l(b).unusedTokens.push(f);
        // add remaining unparsed input length to the string
        l(b).charsLeftOver = i - j, h.length > 0 && l(b).unusedInput.push(h),
            // clear _12h flag if hour is <= 12
            b._a[_d] <= 12 && l(b).bigHour === !0 && b._a[_d] > 0 && (l(b).bigHour = void 0), l(b).parsedDateParts = b._a.slice(0), l(b).meridiem = b._meridiem,
            // handle meridiem
            b._a[_d] = kb(b._locale, b._a[_d], b._meridiem), hb(b), cb(b)
    }

    function kb(a, b, c) {
        var d;
        // Fallback
        return null == c ? b : null != a.meridiemHour ? a.meridiemHour(b, c) : null != a.isPM ? (d = a.isPM(c), d && 12 > b && (b += 12), d || 12 !== b || (b = 0), b) : b
    }
    // date from string and array of format strings
    function lb(a) {
        var b, c, d, e, f;
        if (0 === a._f.length) return l(a).invalidFormat = !0, void(a._d = new Date(NaN));
        for (e = 0; e < a._f.length; e++) f = 0, b = p({}, a), null != a._useUTC && (b._useUTC = a._useUTC), b._f = a._f[e], jb(b), m(b) && (f += l(b).charsLeftOver, f += 10 * l(b).unusedTokens.length, l(b).score = f, (null == d || d > f) && (d = f, c = b));
        i(a, c || b)
    }

    function mb(a) {
        if (!a._d) {
            var b = K(a._i);
            a._a = g([b.year, b.month, b.day || b.date, b.hour, b.minute, b.second, b.millisecond], function(a) {
                return a && parseInt(a, 10)
            }), hb(a)
        }
    }

    function nb(a) {
        var b = new q(cb(ob(a)));
        // Adding is smart enough around DST
        return b._nextDay && (b.add(1, "d"), b._nextDay = void 0), b
    }

    function ob(a) {
        var b = a._i,
            d = a._f;
        return a._locale = a._locale || ab(a._l), null === b || void 0 === d && "" === b ? n({
            nullInput: !0
        }) : ("string" == typeof b && (a._i = b = a._locale.preparse(b)), r(b) ? new q(cb(b)) : (c(d) ? lb(a) : f(b) ? a._d = b : d ? jb(a) : pb(a), m(a) || (a._d = null), a))
    }

    function pb(b) {
        var d = b._i;
        void 0 === d ? b._d = new Date(a.now()) : f(d) ? b._d = new Date(d.valueOf()) : "string" == typeof d ? eb(b) : c(d) ? (b._a = g(d.slice(0), function(a) {
                return parseInt(a, 10)
            }), hb(b)) : "object" == typeof d ? mb(b) : "number" == typeof d ?
            // from milliseconds
            b._d = new Date(d) : a.createFromInputFallback(b)
    }

    function qb(a, b, f, g, h) {
        var i = {};
        // object construction must be done this way.
        // https://github.com/moment/moment/issues/1423
        return "boolean" == typeof f && (g = f, f = void 0), (d(a) && e(a) || c(a) && 0 === a.length) && (a = void 0), i._isAMomentObject = !0, i._useUTC = i._isUTC = h, i._l = f, i._i = a, i._f = b, i._strict = g, nb(i)
    }

    function rb(a, b, c, d) {
        return qb(a, b, c, d, !1)
    }
    // Pick a moment m from moments so that m[fn](other) is true for all
    // other. This relies on the function fn to be transitive.
    //
    // moments should either be an array of moment objects or an array, whose
    // first element is an array of moment objects.
    function sb(a, b) {
        var d, e;
        if (1 === b.length && c(b[0]) && (b = b[0]), !b.length) return rb();
        for (d = b[0], e = 1; e < b.length; ++e) b[e].isValid() && !b[e][a](d) || (d = b[e]);
        return d
    }
    // TODO: Use [].sort instead?
    function tb() {
        var a = [].slice.call(arguments, 0);
        return sb("isBefore", a)
    }

    function ub() {
        var a = [].slice.call(arguments, 0);
        return sb("isAfter", a)
    }

    function vb(a) {
        var b = K(a),
            c = b.year || 0,
            d = b.quarter || 0,
            e = b.month || 0,
            f = b.week || 0,
            g = b.day || 0,
            h = b.hour || 0,
            i = b.minute || 0,
            j = b.second || 0,
            k = b.millisecond || 0;
        // representation for dateAddRemove
        this._milliseconds = +k + 1e3 * j + // 1000
            6e4 * i + // 1000 * 60
            1e3 * h * 60 * 60, //using 1000 * 60 * 60 instead of 36e5 to avoid floating point rounding errors https://github.com/moment/moment/issues/2978
            // Because of dateAddRemove treats 24 hours as different from a
            // day when working around DST, we need to store them separately
            this._days = +g + 7 * f,
            // It is impossible translate months into days without knowing
            // which months you are are talking about, so we have to store
            // it separately.
            this._months = +e + 3 * d + 12 * c, this._data = {}, this._locale = ab(), this._bubble()
    }

    function wb(a) {
        return a instanceof vb
    }
    // FORMATTING
    function xb(a, b) {
        T(a, 0, 0, function() {
            var a = this.utcOffset(),
                c = "+";
            return 0 > a && (a = -a, c = "-"), c + S(~~(a / 60), 2) + b + S(~~a % 60, 2)
        })
    }

    function yb(a, b) {
        var c = (b || "").match(a) || [],
            d = c[c.length - 1] || [],
            e = (d + "").match(Ge) || ["-", 0, 0],
            f = +(60 * e[1]) + t(e[2]);
        return "+" === e[0] ? f : -f
    }
    // Return a moment from input, that is local/utc/zone equivalent to model.
    function zb(b, c) {
        var d, e;
        // Use low-level api, because this fn is low-level api.
        return c._isUTC ? (d = c.clone(), e = (r(b) || f(b) ? b.valueOf() : rb(b).valueOf()) - d.valueOf(), d._d.setTime(d._d.valueOf() + e), a.updateOffset(d, !1), d) : rb(b).local()
    }

    function Ab(a) {
        // On Firefox.24 Date#getTimezoneOffset returns a floating point.
        // https://github.com/moment/moment/pull/1871
        return 15 * -Math.round(a._d.getTimezoneOffset() / 15)
    }
    // MOMENTS
    // keepLocalTime = true means only change the timezone, without
    // affecting the local hour. So 5:31:26 +0300 --[utcOffset(2, true)]-->
    // 5:31:26 +0200 It is possible that 5:31:26 doesn't exist with offset
    // +0200, so we adjust the time as needed, to be valid.
    //
    // Keeping the time actually adds/subtracts (one hour)
    // from the actual represented time. That is why we call updateOffset
    // a second time. In case it wants us to change the offset again
    // _changeInProgress == true case, then we have to adjust, because
    // there is no such time in the given timezone.
    function Bb(b, c) {
        var d, e = this._offset || 0;
        return this.isValid() ? null != b ? ("string" == typeof b ? b = yb(Td, b) : Math.abs(b) < 16 && (b = 60 * b), !this._isUTC && c && (d = Ab(this)), this._offset = b, this._isUTC = !0, null != d && this.add(d, "m"), e !== b && (!c || this._changeInProgress ? Sb(this, Mb(b - e, "m"), 1, !1) : this._changeInProgress || (this._changeInProgress = !0, a.updateOffset(this, !0), this._changeInProgress = null)), this) : this._isUTC ? e : Ab(this) : null != b ? this : NaN
    }

    function Cb(a, b) {
        return null != a ? ("string" != typeof a && (a = -a), this.utcOffset(a, b), this) : -this.utcOffset()
    }

    function Db(a) {
        return this.utcOffset(0, a)
    }

    function Eb(a) {
        return this._isUTC && (this.utcOffset(0, a), this._isUTC = !1, a && this.subtract(Ab(this), "m")), this
    }

    function Fb() {
        return this._tzm ? this.utcOffset(this._tzm) : "string" == typeof this._i && this.utcOffset(yb(Sd, this._i)), this
    }

    function Gb(a) {
        return this.isValid() ? (a = a ? rb(a).utcOffset() : 0, (this.utcOffset() - a) % 60 === 0) : !1
    }

    function Hb() {
        return this.utcOffset() > this.clone().month(0).utcOffset() || this.utcOffset() > this.clone().month(5).utcOffset()
    }

    function Ib() {
        if (!o(this._isDSTShifted)) return this._isDSTShifted;
        var a = {};
        if (p(a, this), a = ob(a), a._a) {
            var b = a._isUTC ? j(a._a) : rb(a._a);
            this._isDSTShifted = this.isValid() && u(a._a, b.toArray()) > 0
        } else this._isDSTShifted = !1;
        return this._isDSTShifted
    }

    function Jb() {
        return this.isValid() ? !this._isUTC : !1
    }

    function Kb() {
        return this.isValid() ? this._isUTC : !1
    }

    function Lb() {
        return this.isValid() ? this._isUTC && 0 === this._offset : !1
    }

    function Mb(a, b) {
        var c, d, e, f = a,
            // matching against regexp is expensive, do it on demand
            g = null; // checks for null or undefined
        return wb(a) ? f = {
            ms: a._milliseconds,
            d: a._days,
            M: a._months
        } : "number" == typeof a ? (f = {}, b ? f[b] = a : f.milliseconds = a) : (g = He.exec(a)) ? (c = "-" === g[1] ? -1 : 1, f = {
            y: 0,
            d: t(g[$d]) * c,
            h: t(g[_d]) * c,
            m: t(g[ae]) * c,
            s: t(g[be]) * c,
            ms: t(g[ce]) * c
        }) : (g = Ie.exec(a)) ? (c = "-" === g[1] ? -1 : 1, f = {
            y: Nb(g[2], c),
            M: Nb(g[3], c),
            w: Nb(g[4], c),
            d: Nb(g[5], c),
            h: Nb(g[6], c),
            m: Nb(g[7], c),
            s: Nb(g[8], c)
        }) : null == f ? f = {} : "object" == typeof f && ("from" in f || "to" in f) && (e = Pb(rb(f.from), rb(f.to)), f = {}, f.ms = e.milliseconds, f.M = e.months), d = new vb(f), wb(a) && h(a, "_locale") && (d._locale = a._locale), d
    }

    function Nb(a, b) {
        // We'd normally use ~~inp for this, but unfortunately it also
        // converts floats to ints.
        // inp may be undefined, so careful calling replace on it.
        var c = a && parseFloat(a.replace(",", "."));
        // apply sign while we're at it
        return (isNaN(c) ? 0 : c) * b
    }

    function Ob(a, b) {
        var c = {
            milliseconds: 0,
            months: 0
        };
        return c.months = b.month() - a.month() + 12 * (b.year() - a.year()), a.clone().add(c.months, "M").isAfter(b) && --c.months, c.milliseconds = +b - +a.clone().add(c.months, "M"), c
    }

    function Pb(a, b) {
        var c;
        return a.isValid() && b.isValid() ? (b = zb(b, a), a.isBefore(b) ? c = Ob(a, b) : (c = Ob(b, a), c.milliseconds = -c.milliseconds, c.months = -c.months), c) : {
            milliseconds: 0,
            months: 0
        }
    }

    function Qb(a) {
        return 0 > a ? -1 * Math.round(-1 * a) : Math.round(a)
    }
    // TODO: remove 'name' arg after deprecation is removed
    function Rb(a, b) {
        return function(c, d) {
            var e, f;
            //invert the arguments, but complain about it
            return null === d || isNaN(+d) || (x(b, "moment()." + b + "(period, number) is deprecated. Please use moment()." + b + "(number, period). See http://momentjs.com/guides/#/warnings/add-inverted-param/ for more info."), f = c, c = d, d = f), c = "string" == typeof c ? +c : c, e = Mb(c, d), Sb(this, e, a), this
        }
    }

    function Sb(b, c, d, e) {
        var f = c._milliseconds,
            g = Qb(c._days),
            h = Qb(c._months);
        b.isValid() && (e = null == e ? !0 : e, f && b._d.setTime(b._d.valueOf() + f * d), g && P(b, "Date", O(b, "Date") + g * d), h && ia(b, O(b, "Month") + h * d), e && a.updateOffset(b, g || h))
    }

    function Tb(a, b) {
        var c = a.diff(b, "days", !0);
        return -6 > c ? "sameElse" : -1 > c ? "lastWeek" : 0 > c ? "lastDay" : 1 > c ? "sameDay" : 2 > c ? "nextDay" : 7 > c ? "nextWeek" : "sameElse"
    }

    function Ub(b, c) {
        // We want to compare the start of today, vs this.
        // Getting start-of-today depends on whether we're local/utc/offset or not.
        var d = b || rb(),
            e = zb(d, this).startOf("day"),
            f = a.calendarFormat(this, e) || "sameElse",
            g = c && (y(c[f]) ? c[f].call(this, d) : c[f]);
        return this.format(g || this.localeData().calendar(f, this, rb(d)))
    }

    function Vb() {
        return new q(this)
    }

    function Wb(a, b) {
        var c = r(a) ? a : rb(a);
        return this.isValid() && c.isValid() ? (b = J(o(b) ? "millisecond" : b), "millisecond" === b ? this.valueOf() > c.valueOf() : c.valueOf() < this.clone().startOf(b).valueOf()) : !1
    }

    function Xb(a, b) {
        var c = r(a) ? a : rb(a);
        return this.isValid() && c.isValid() ? (b = J(o(b) ? "millisecond" : b), "millisecond" === b ? this.valueOf() < c.valueOf() : this.clone().endOf(b).valueOf() < c.valueOf()) : !1
    }

    function Yb(a, b, c, d) {
        return d = d || "()", ("(" === d[0] ? this.isAfter(a, c) : !this.isBefore(a, c)) && (")" === d[1] ? this.isBefore(b, c) : !this.isAfter(b, c))
    }

    function Zb(a, b) {
        var c, d = r(a) ? a : rb(a);
        return this.isValid() && d.isValid() ? (b = J(b || "millisecond"), "millisecond" === b ? this.valueOf() === d.valueOf() : (c = d.valueOf(), this.clone().startOf(b).valueOf() <= c && c <= this.clone().endOf(b).valueOf())) : !1
    }

    function $b(a, b) {
        return this.isSame(a, b) || this.isAfter(a, b)
    }

    function _b(a, b) {
        return this.isSame(a, b) || this.isBefore(a, b)
    }

    function ac(a, b, c) {
        var d, e, f, g; // 1000
        // 1000 * 60
        // 1000 * 60 * 60
        // 1000 * 60 * 60 * 24, negate dst
        // 1000 * 60 * 60 * 24 * 7, negate dst
        return this.isValid() ? (d = zb(a, this), d.isValid() ? (e = 6e4 * (d.utcOffset() - this.utcOffset()), b = J(b), "year" === b || "month" === b || "quarter" === b ? (g = bc(this, d), "quarter" === b ? g /= 3 : "year" === b && (g /= 12)) : (f = this - d, g = "second" === b ? f / 1e3 : "minute" === b ? f / 6e4 : "hour" === b ? f / 36e5 : "day" === b ? (f - e) / 864e5 : "week" === b ? (f - e) / 6048e5 : f), c ? g : s(g)) : NaN) : NaN
    }

    function bc(a, b) {
        // difference in months
        var c, d, e = 12 * (b.year() - a.year()) + (b.month() - a.month()),
            // b is in (anchor - 1 month, anchor + 1 month)
            f = a.clone().add(e, "months");
        //check for negative zero, return zero if negative zero
        // linear across the month
        // linear across the month
        return 0 > b - f ? (c = a.clone().add(e - 1, "months"), d = (b - f) / (f - c)) : (c = a.clone().add(e + 1, "months"), d = (b - f) / (c - f)), -(e + d) || 0
    }

    function cc() {
        return this.clone().locale("en").format("ddd MMM DD YYYY HH:mm:ss [GMT]ZZ")
    }

    function dc() {
        var a = this.clone().utc();
        return 0 < a.year() && a.year() <= 9999 ? y(Date.prototype.toISOString) ? this.toDate().toISOString() : W(a, "YYYY-MM-DD[T]HH:mm:ss.SSS[Z]") : W(a, "YYYYYY-MM-DD[T]HH:mm:ss.SSS[Z]")
    }

    function ec(b) {
        b || (b = this.isUtc() ? a.defaultFormatUtc : a.defaultFormat);
        var c = W(this, b);
        return this.localeData().postformat(c)
    }

    function fc(a, b) {
        return this.isValid() && (r(a) && a.isValid() || rb(a).isValid()) ? Mb({
            to: this,
            from: a
        }).locale(this.locale()).humanize(!b) : this.localeData().invalidDate()
    }

    function gc(a) {
        return this.from(rb(), a)
    }

    function hc(a, b) {
        return this.isValid() && (r(a) && a.isValid() || rb(a).isValid()) ? Mb({
            from: this,
            to: a
        }).locale(this.locale()).humanize(!b) : this.localeData().invalidDate()
    }

    function ic(a) {
        return this.to(rb(), a)
    }
    // If passed a locale key, it will set the locale for this
    // instance.  Otherwise, it will return the locale configuration
    // variables for this instance.
    function jc(a) {
        var b;
        return void 0 === a ? this._locale._abbr : (b = ab(a), null != b && (this._locale = b), this)
    }

    function kc() {
        return this._locale
    }

    function lc(a) {
        // the following switch intentionally omits break keywords
        // to utilize falling through the cases.
        switch (a = J(a)) {
            case "year":
                this.month(0); /* falls through */
            case "quarter":
            case "month":
                this.date(1); /* falls through */
            case "week":
            case "isoWeek":
            case "day":
            case "date":
                this.hours(0); /* falls through */
            case "hour":
                this.minutes(0); /* falls through */
            case "minute":
                this.seconds(0); /* falls through */
            case "second":
                this.milliseconds(0)
        }
        // weeks are a special case
        // quarters are also special
        return "week" === a && this.weekday(0), "isoWeek" === a && this.isoWeekday(1), "quarter" === a && this.month(3 * Math.floor(this.month() / 3)), this
    }

    function mc(a) {
        // 'date' is an alias for 'day', so it should be considered as such.
        return a = J(a), void 0 === a || "millisecond" === a ? this : ("date" === a && (a = "day"), this.startOf(a).add(1, "isoWeek" === a ? "week" : a).subtract(1, "ms"))
    }

    function nc() {
        return this._d.valueOf() - 6e4 * (this._offset || 0)
    }

    function oc() {
        return Math.floor(this.valueOf() / 1e3)
    }

    function pc() {
        return new Date(this.valueOf())
    }

    function qc() {
        var a = this;
        return [a.year(), a.month(), a.date(), a.hour(), a.minute(), a.second(), a.millisecond()]
    }

    function rc() {
        var a = this;
        return {
            years: a.year(),
            months: a.month(),
            date: a.date(),
            hours: a.hours(),
            minutes: a.minutes(),
            seconds: a.seconds(),
            milliseconds: a.milliseconds()
        }
    }

    function sc() {
        // new Date(NaN).toJSON() === null
        return this.isValid() ? this.toISOString() : null
    }

    function tc() {
        return m(this)
    }

    function uc() {
        return i({}, l(this))
    }

    function vc() {
        return l(this).overflow
    }

    function wc() {
        return {
            input: this._i,
            format: this._f,
            locale: this._locale,
            isUTC: this._isUTC,
            strict: this._strict
        }
    }

    function xc(a, b) {
        T(0, [a, a.length], 0, b)
    }
    // MOMENTS
    function yc(a) {
        return Cc.call(this, a, this.week(), this.weekday(), this.localeData()._week.dow, this.localeData()._week.doy)
    }

    function zc(a) {
        return Cc.call(this, a, this.isoWeek(), this.isoWeekday(), 1, 4)
    }

    function Ac() {
        return wa(this.year(), 1, 4)
    }

    function Bc() {
        var a = this.localeData()._week;
        return wa(this.year(), a.dow, a.doy)
    }

    function Cc(a, b, c, d, e) {
        var f;
        return null == a ? va(this, d, e).year : (f = wa(a, d, e), b > f && (b = f), Dc.call(this, a, b, c, d, e))
    }

    function Dc(a, b, c, d, e) {
        var f = ua(a, b, c, d, e),
            g = sa(f.year, 0, f.dayOfYear);
        return this.year(g.getUTCFullYear()), this.month(g.getUTCMonth()), this.date(g.getUTCDate()), this
    }
    // MOMENTS
    function Ec(a) {
        return null == a ? Math.ceil((this.month() + 1) / 3) : this.month(3 * (a - 1) + this.month() % 3)
    }
    // HELPERS
    // MOMENTS
    function Fc(a) {
        var b = Math.round((this.clone().startOf("day") - this.clone().startOf("year")) / 864e5) + 1;
        return null == a ? b : this.add(a - b, "d")
    }

    function Gc(a, b) {
        b[ce] = t(1e3 * ("0." + a))
    }
    // MOMENTS
    function Hc() {
        return this._isUTC ? "UTC" : ""
    }

    function Ic() {
        return this._isUTC ? "Coordinated Universal Time" : ""
    }

    function Jc(a) {
        return rb(1e3 * a)
    }

    function Kc() {
        return rb.apply(null, arguments).parseZone()
    }

    function Lc(a) {
        return a
    }

    function Mc(a, b, c, d) {
        var e = ab(),
            f = j().set(d, b);
        return e[c](f, a)
    }

    function Nc(a, b, c) {
        if ("number" == typeof a && (b = a, a = void 0), a = a || "", null != b) return Mc(a, b, c, "month");
        var d, e = [];
        for (d = 0; 12 > d; d++) e[d] = Mc(a, d, c, "month");
        return e
    }
    // ()
    // (5)
    // (fmt, 5)
    // (fmt)
    // (true)
    // (true, 5)
    // (true, fmt, 5)
    // (true, fmt)
    function Oc(a, b, c, d) {
        "boolean" == typeof a ? ("number" == typeof b && (c = b, b = void 0), b = b || "") : (b = a, c = b, a = !1, "number" == typeof b && (c = b, b = void 0), b = b || "");
        var e = ab(),
            f = a ? e._week.dow : 0;
        if (null != c) return Mc(b, (c + f) % 7, d, "day");
        var g, h = [];
        for (g = 0; 7 > g; g++) h[g] = Mc(b, (g + f) % 7, d, "day");
        return h
    }

    function Pc(a, b) {
        return Nc(a, b, "months")
    }

    function Qc(a, b) {
        return Nc(a, b, "monthsShort")
    }

    function Rc(a, b, c) {
        return Oc(a, b, c, "weekdays")
    }

    function Sc(a, b, c) {
        return Oc(a, b, c, "weekdaysShort")
    }

    function Tc(a, b, c) {
        return Oc(a, b, c, "weekdaysMin")
    }

    function Uc() {
        var a = this._data;
        return this._milliseconds = Ue(this._milliseconds), this._days = Ue(this._days), this._months = Ue(this._months), a.milliseconds = Ue(a.milliseconds), a.seconds = Ue(a.seconds), a.minutes = Ue(a.minutes), a.hours = Ue(a.hours), a.months = Ue(a.months), a.years = Ue(a.years), this
    }

    function Vc(a, b, c, d) {
        var e = Mb(b, c);
        return a._milliseconds += d * e._milliseconds, a._days += d * e._days, a._months += d * e._months, a._bubble()
    }
    // supports only 2.0-style add(1, 's') or add(duration)
    function Wc(a, b) {
        return Vc(this, a, b, 1)
    }
    // supports only 2.0-style subtract(1, 's') or subtract(duration)
    function Xc(a, b) {
        return Vc(this, a, b, -1)
    }

    function Yc(a) {
        return 0 > a ? Math.floor(a) : Math.ceil(a)
    }

    function Zc() {
        var a, b, c, d, e, f = this._milliseconds,
            g = this._days,
            h = this._months,
            i = this._data;
        // if we have a mix of positive and negative values, bubble down first
        // check: https://github.com/moment/moment/issues/2166
        // The following code bubbles up values, see the tests for
        // examples of what that means.
        // convert days to months
        // 12 months -> 1 year
        return f >= 0 && g >= 0 && h >= 0 || 0 >= f && 0 >= g && 0 >= h || (f += 864e5 * Yc(_c(h) + g), g = 0, h = 0), i.milliseconds = f % 1e3, a = s(f / 1e3), i.seconds = a % 60, b = s(a / 60), i.minutes = b % 60, c = s(b / 60), i.hours = c % 24, g += s(c / 24), e = s($c(g)), h += e, g -= Yc(_c(e)), d = s(h / 12), h %= 12, i.days = g, i.months = h, i.years = d, this
    }

    function $c(a) {
        // 400 years have 146097 days (taking into account leap year rules)
        // 400 years have 12 months === 4800
        return 4800 * a / 146097
    }

    function _c(a) {
        // the reverse of daysToMonths
        return 146097 * a / 4800
    }

    function ad(a) {
        var b, c, d = this._milliseconds;
        if (a = J(a), "month" === a || "year" === a) return b = this._days + d / 864e5, c = this._months + $c(b), "month" === a ? c : c / 12;
        switch (b = this._days + Math.round(_c(this._months)), a) {
            case "week":
                return b / 7 + d / 6048e5;
            case "day":
                return b + d / 864e5;
            case "hour":
                return 24 * b + d / 36e5;
            case "minute":
                return 1440 * b + d / 6e4;
            case "second":
                return 86400 * b + d / 1e3;
                // Math.floor prevents floating point math errors here
            case "millisecond":
                return Math.floor(864e5 * b) + d;
            default:
                throw new Error("Unknown unit " + a)
        }
    }
    // TODO: Use this.as('ms')?
    function bd() {
        return this._milliseconds + 864e5 * this._days + this._months % 12 * 2592e6 + 31536e6 * t(this._months / 12)
    }

    function cd(a) {
        return function() {
            return this.as(a)
        }
    }

    function dd(a) {
        return a = J(a), this[a + "s"]()
    }

    function ed(a) {
        return function() {
            return this._data[a]
        }
    }

    function fd() {
        return s(this.days() / 7)
    }
    // helper function for moment.fn.from, moment.fn.fromNow, and moment.duration.fn.humanize
    function gd(a, b, c, d, e) {
        return e.relativeTime(b || 1, !!c, a, d)
    }

    function hd(a, b, c) {
        var d = Mb(a).abs(),
            e = jf(d.as("s")),
            f = jf(d.as("m")),
            g = jf(d.as("h")),
            h = jf(d.as("d")),
            i = jf(d.as("M")),
            j = jf(d.as("y")),
            k = e < kf.s && ["s", e] || 1 >= f && ["m"] || f < kf.m && ["mm", f] || 1 >= g && ["h"] || g < kf.h && ["hh", g] || 1 >= h && ["d"] || h < kf.d && ["dd", h] || 1 >= i && ["M"] || i < kf.M && ["MM", i] || 1 >= j && ["y"] || ["yy", j];
        return k[2] = b, k[3] = +a > 0, k[4] = c, gd.apply(null, k)
    }
    // This function allows you to set the rounding function for relative time strings
    function id(a) {
        return void 0 === a ? jf : "function" == typeof a ? (jf = a, !0) : !1
    }
    // This function allows you to set a threshold for relative time strings
    function jd(a, b) {
        return void 0 === kf[a] ? !1 : void 0 === b ? kf[a] : (kf[a] = b, !0)
    }

    function kd(a) {
        var b = this.localeData(),
            c = hd(this, !a, b);
        return a && (c = b.pastFuture(+this, c)), b.postformat(c)
    }

    function ld() {
        // for ISO strings we do not use the normal bubbling rules:
        //  * milliseconds bubble up until they become hours
        //  * days do not bubble at all
        //  * months bubble up until they become years
        // This is because there is no context-free conversion between hours and days
        // (think of clock changes)
        // and also not between days and months (28-31 days per month)
        var a, b, c, d = lf(this._milliseconds) / 1e3,
            e = lf(this._days),
            f = lf(this._months);
        a = s(d / 60), b = s(a / 60), d %= 60, a %= 60, c = s(f / 12), f %= 12;
        // inspired by https://github.com/dordille/moment-isoduration/blob/master/moment.isoduration.js
        var g = c,
            h = f,
            i = e,
            j = b,
            k = a,
            l = d,
            m = this.asSeconds();
        return m ? (0 > m ? "-" : "") + "P" + (g ? g + "Y" : "") + (h ? h + "M" : "") + (i ? i + "D" : "") + (j || k || l ? "T" : "") + (j ? j + "H" : "") + (k ? k + "M" : "") + (l ? l + "S" : "") : "P0D"
    }
    var md, nd;
    nd = Array.prototype.some ? Array.prototype.some : function(a) {
        for (var b = Object(this), c = b.length >>> 0, d = 0; c > d; d++)
            if (d in b && a.call(this, b[d], d, b)) return !0;
        return !1
    };
    // Plugins that add properties should also add the key here (null value),
    // so we can properly clone ourselves.
    var od = a.momentProperties = [],
        pd = !1,
        qd = {};
    a.suppressDeprecationWarnings = !1, a.deprecationHandler = null;
    var rd;
    rd = Object.keys ? Object.keys : function(a) {
        var b, c = [];
        for (b in a) h(a, b) && c.push(b);
        return c
    };
    var sd, td = {
            sameDay: "[Today at] LT",
            nextDay: "[Tomorrow at] LT",
            nextWeek: "dddd [at] LT",
            lastDay: "[Yesterday at] LT",
            lastWeek: "[Last] dddd [at] LT",
            sameElse: "L"
        },
        ud = {
            LTS: "h:mm:ss A",
            LT: "h:mm A",
            L: "MM/DD/YYYY",
            LL: "MMMM D, YYYY",
            LLL: "MMMM D, YYYY h:mm A",
            LLLL: "dddd, MMMM D, YYYY h:mm A"
        },
        vd = "Invalid date",
        wd = "%d",
        xd = /\d{1,2}/,
        yd = {
            future: "in %s",
            past: "%s ago",
            s: "a few seconds",
            m: "a minute",
            mm: "%d minutes",
            h: "an hour",
            hh: "%d hours",
            d: "a day",
            dd: "%d days",
            M: "a month",
            MM: "%d months",
            y: "a year",
            yy: "%d years"
        },
        zd = {},
        Ad = {},
        Bd = /(\[[^\[]*\])|(\\)?([Hh]mm(ss)?|Mo|MM?M?M?|Do|DDDo|DD?D?D?|ddd?d?|do?|w[o|w]?|W[o|W]?|Qo?|YYYYYY|YYYYY|YYYY|YY|gg(ggg?)?|GG(GGG?)?|e|E|a|A|hh?|HH?|kk?|mm?|ss?|S{1,9}|x|X|zz?|ZZ?|.)/g,
        Cd = /(\[[^\[]*\])|(\\)?(LTS|LT|LL?L?L?|l{1,4})/g,
        Dd = {},
        Ed = {},
        Fd = /\d/,
        Gd = /\d\d/,
        Hd = /\d{3}/,
        Id = /\d{4}/,
        Jd = /[+-]?\d{6}/,
        Kd = /\d\d?/,
        Ld = /\d\d\d\d?/,
        Md = /\d\d\d\d\d\d?/,
        Nd = /\d{1,3}/,
        Od = /\d{1,4}/,
        Pd = /[+-]?\d{1,6}/,
        Qd = /\d+/,
        Rd = /[+-]?\d+/,
        Sd = /Z|[+-]\d\d:?\d\d/gi,
        Td = /Z|[+-]\d\d(?::?\d\d)?/gi,
        Ud = /[+-]?\d+(\.\d{1,3})?/,
        Vd = /[0-9]*['a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+|[\u0600-\u06FF\/]+(\s*?[\u0600-\u06FF]+){1,2}/i,
        Wd = {},
        Xd = {},
        Yd = 0,
        Zd = 1,
        $d = 2,
        _d = 3,
        ae = 4,
        be = 5,
        ce = 6,
        de = 7,
        ee = 8;
    sd = Array.prototype.indexOf ? Array.prototype.indexOf : function(a) {
        // I know
        var b;
        for (b = 0; b < this.length; ++b)
            if (this[b] === a) return b;
        return -1
    }, T("M", ["MM", 2], "Mo", function() {
        return this.month() + 1
    }), T("MMM", 0, 0, function(a) {
        return this.localeData().monthsShort(this, a)
    }), T("MMMM", 0, 0, function(a) {
        return this.localeData().months(this, a)
    }), I("month", "M"), L("month", 8), Y("M", Kd), Y("MM", Kd, Gd), Y("MMM", function(a, b) {
        return b.monthsShortRegex(a)
    }), Y("MMMM", function(a, b) {
        return b.monthsRegex(a)
    }), aa(["M", "MM"], function(a, b) {
        b[Zd] = t(a) - 1
    }), aa(["MMM", "MMMM"], function(a, b, c, d) {
        var e = c._locale.monthsParse(a, d, c._strict);
        null != e ? b[Zd] = e : l(c).invalidMonth = a
    });
    // LOCALES
    var fe = /D[oD]?(\[[^\[\]]*\]|\s+)+MMMM?/,
        ge = "January_February_March_April_May_June_July_August_September_October_November_December".split("_"),
        he = "Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),
        ie = Vd,
        je = Vd;
    // FORMATTING
    T("Y", 0, 0, function() {
            var a = this.year();
            return 9999 >= a ? "" + a : "+" + a
        }), T(0, ["YY", 2], 0, function() {
            return this.year() % 100
        }), T(0, ["YYYY", 4], 0, "year"), T(0, ["YYYYY", 5], 0, "year"), T(0, ["YYYYYY", 6, !0], 0, "year"),
        // ALIASES
        I("year", "y"),
        // PRIORITIES
        L("year", 1),
        // PARSING
        Y("Y", Rd), Y("YY", Kd, Gd), Y("YYYY", Od, Id), Y("YYYYY", Pd, Jd), Y("YYYYYY", Pd, Jd), aa(["YYYYY", "YYYYYY"], Yd), aa("YYYY", function(b, c) {
            c[Yd] = 2 === b.length ? a.parseTwoDigitYear(b) : t(b)
        }), aa("YY", function(b, c) {
            c[Yd] = a.parseTwoDigitYear(b)
        }), aa("Y", function(a, b) {
            b[Yd] = parseInt(a, 10)
        }),
        // HOOKS
        a.parseTwoDigitYear = function(a) {
            return t(a) + (t(a) > 68 ? 1900 : 2e3)
        };
    // MOMENTS
    var ke = N("FullYear", !0);
    // FORMATTING
    T("w", ["ww", 2], "wo", "week"), T("W", ["WW", 2], "Wo", "isoWeek"),
        // ALIASES
        I("week", "w"), I("isoWeek", "W"),
        // PRIORITIES
        L("week", 5), L("isoWeek", 5),
        // PARSING
        Y("w", Kd), Y("ww", Kd, Gd), Y("W", Kd), Y("WW", Kd, Gd), ba(["w", "ww", "W", "WW"], function(a, b, c, d) {
            b[d.substr(0, 1)] = t(a)
        });
    var le = {
        dow: 0, // Sunday is the first day of the week.
        doy: 6
    };
    // FORMATTING
    T("d", 0, "do", "day"), T("dd", 0, 0, function(a) {
            return this.localeData().weekdaysMin(this, a)
        }), T("ddd", 0, 0, function(a) {
            return this.localeData().weekdaysShort(this, a)
        }), T("dddd", 0, 0, function(a) {
            return this.localeData().weekdays(this, a)
        }), T("e", 0, 0, "weekday"), T("E", 0, 0, "isoWeekday"),
        // ALIASES
        I("day", "d"), I("weekday", "e"), I("isoWeekday", "E"),
        // PRIORITY
        L("day", 11), L("weekday", 11), L("isoWeekday", 11),
        // PARSING
        Y("d", Kd), Y("e", Kd), Y("E", Kd), Y("dd", function(a, b) {
            return b.weekdaysMinRegex(a)
        }), Y("ddd", function(a, b) {
            return b.weekdaysShortRegex(a)
        }), Y("dddd", function(a, b) {
            return b.weekdaysRegex(a)
        }), ba(["dd", "ddd", "dddd"], function(a, b, c, d) {
            var e = c._locale.weekdaysParse(a, d, c._strict);
            // if we didn't get a weekday name, mark the date as invalid
            null != e ? b.d = e : l(c).invalidWeekday = a
        }), ba(["d", "e", "E"], function(a, b, c, d) {
            b[d] = t(a)
        });
    // LOCALES
    var me = "Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),
        ne = "Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),
        oe = "Su_Mo_Tu_We_Th_Fr_Sa".split("_"),
        pe = Vd,
        qe = Vd,
        re = Vd;
    T("H", ["HH", 2], 0, "hour"), T("h", ["hh", 2], 0, Qa), T("k", ["kk", 2], 0, Ra), T("hmm", 0, 0, function() {
            return "" + Qa.apply(this) + S(this.minutes(), 2)
        }), T("hmmss", 0, 0, function() {
            return "" + Qa.apply(this) + S(this.minutes(), 2) + S(this.seconds(), 2)
        }), T("Hmm", 0, 0, function() {
            return "" + this.hours() + S(this.minutes(), 2)
        }), T("Hmmss", 0, 0, function() {
            return "" + this.hours() + S(this.minutes(), 2) + S(this.seconds(), 2)
        }), Sa("a", !0), Sa("A", !1),
        // ALIASES
        I("hour", "h"),
        // PRIORITY
        L("hour", 13), Y("a", Ta), Y("A", Ta), Y("H", Kd), Y("h", Kd), Y("HH", Kd, Gd), Y("hh", Kd, Gd), Y("hmm", Ld), Y("hmmss", Md), Y("Hmm", Ld), Y("Hmmss", Md), aa(["H", "HH"], _d), aa(["a", "A"], function(a, b, c) {
            c._isPm = c._locale.isPM(a), c._meridiem = a
        }), aa(["h", "hh"], function(a, b, c) {
            b[_d] = t(a), l(c).bigHour = !0
        }), aa("hmm", function(a, b, c) {
            var d = a.length - 2;
            b[_d] = t(a.substr(0, d)), b[ae] = t(a.substr(d)), l(c).bigHour = !0
        }), aa("hmmss", function(a, b, c) {
            var d = a.length - 4,
                e = a.length - 2;
            b[_d] = t(a.substr(0, d)), b[ae] = t(a.substr(d, 2)), b[be] = t(a.substr(e)), l(c).bigHour = !0
        }), aa("Hmm", function(a, b, c) {
            var d = a.length - 2;
            b[_d] = t(a.substr(0, d)), b[ae] = t(a.substr(d))
        }), aa("Hmmss", function(a, b, c) {
            var d = a.length - 4,
                e = a.length - 2;
            b[_d] = t(a.substr(0, d)), b[ae] = t(a.substr(d, 2)), b[be] = t(a.substr(e))
        });
    var se, te = /[ap]\.?m?\.?/i,
        ue = N("Hours", !0),
        ve = {
            calendar: td,
            longDateFormat: ud,
            invalidDate: vd,
            ordinal: wd,
            ordinalParse: xd,
            relativeTime: yd,
            months: ge,
            monthsShort: he,
            week: le,
            weekdays: me,
            weekdaysMin: oe,
            weekdaysShort: ne,
            meridiemParse: te
        },
        we = {},
        xe = /^\s*((?:[+-]\d{6}|\d{4})-(?:\d\d-\d\d|W\d\d-\d|W\d\d|\d\d\d|\d\d))(?:(T| )(\d\d(?::\d\d(?::\d\d(?:[.,]\d+)?)?)?)([\+\-]\d\d(?::?\d\d)?|\s*Z)?)?/,
        ye = /^\s*((?:[+-]\d{6}|\d{4})(?:\d\d\d\d|W\d\d\d|W\d\d|\d\d\d|\d\d))(?:(T| )(\d\d(?:\d\d(?:\d\d(?:[.,]\d+)?)?)?)([\+\-]\d\d(?::?\d\d)?|\s*Z)?)?/,
        ze = /Z|[+-]\d\d(?::?\d\d)?/,
        Ae = [
            ["YYYYYY-MM-DD", /[+-]\d{6}-\d\d-\d\d/],
            ["YYYY-MM-DD", /\d{4}-\d\d-\d\d/],
            ["GGGG-[W]WW-E", /\d{4}-W\d\d-\d/],
            ["GGGG-[W]WW", /\d{4}-W\d\d/, !1],
            ["YYYY-DDD", /\d{4}-\d{3}/],
            ["YYYY-MM", /\d{4}-\d\d/, !1],
            ["YYYYYYMMDD", /[+-]\d{10}/],
            ["YYYYMMDD", /\d{8}/],
            // YYYYMM is NOT allowed by the standard
            ["GGGG[W]WWE", /\d{4}W\d{3}/],
            ["GGGG[W]WW", /\d{4}W\d{2}/, !1],
            ["YYYYDDD", /\d{7}/]
        ],
        Be = [
            ["HH:mm:ss.SSSS", /\d\d:\d\d:\d\d\.\d+/],
            ["HH:mm:ss,SSSS", /\d\d:\d\d:\d\d,\d+/],
            ["HH:mm:ss", /\d\d:\d\d:\d\d/],
            ["HH:mm", /\d\d:\d\d/],
            ["HHmmss.SSSS", /\d\d\d\d\d\d\.\d+/],
            ["HHmmss,SSSS", /\d\d\d\d\d\d,\d+/],
            ["HHmmss", /\d\d\d\d\d\d/],
            ["HHmm", /\d\d\d\d/],
            ["HH", /\d\d/]
        ],
        Ce = /^\/?Date\((\-?\d+)/i;
    a.createFromInputFallback = w("moment construction falls back to js Date. This is discouraged and will be removed in upcoming major release. Please refer to http://momentjs.com/guides/#/warnings/js-date/ for more info.", function(a) {
            a._d = new Date(a._i + (a._useUTC ? " UTC" : ""))
        }),
        // constant that refers to the ISO standard
        a.ISO_8601 = function() {};
    var De = w("moment().min is deprecated, use moment.max instead. http://momentjs.com/guides/#/warnings/min-max/", function() {
            var a = rb.apply(null, arguments);
            return this.isValid() && a.isValid() ? this > a ? this : a : n()
        }),
        Ee = w("moment().max is deprecated, use moment.min instead. http://momentjs.com/guides/#/warnings/min-max/", function() {
            var a = rb.apply(null, arguments);
            return this.isValid() && a.isValid() ? a > this ? this : a : n()
        }),
        Fe = function() {
            return Date.now ? Date.now() : +new Date
        };
    xb("Z", ":"), xb("ZZ", ""),
        // PARSING
        Y("Z", Td), Y("ZZ", Td), aa(["Z", "ZZ"], function(a, b, c) {
            c._useUTC = !0, c._tzm = yb(Td, a)
        });
    // HELPERS
    // timezone chunker
    // '+10:00' > ['10',  '00']
    // '-1530'  > ['-15', '30']
    var Ge = /([\+\-]|\d\d)/gi;
    // HOOKS
    // This function will be called whenever a moment is mutated.
    // It is intended to keep the offset in sync with the timezone.
    a.updateOffset = function() {};
    // ASP.NET json date format regex
    var He = /^(\-)?(?:(\d*)[. ])?(\d+)\:(\d+)(?:\:(\d+)\.?(\d{3})?\d*)?$/,
        Ie = /^(-)?P(?:(-?[0-9,.]*)Y)?(?:(-?[0-9,.]*)M)?(?:(-?[0-9,.]*)W)?(?:(-?[0-9,.]*)D)?(?:T(?:(-?[0-9,.]*)H)?(?:(-?[0-9,.]*)M)?(?:(-?[0-9,.]*)S)?)?$/;
    Mb.fn = vb.prototype;
    var Je = Rb(1, "add"),
        Ke = Rb(-1, "subtract");
    a.defaultFormat = "YYYY-MM-DDTHH:mm:ssZ", a.defaultFormatUtc = "YYYY-MM-DDTHH:mm:ss[Z]";
    var Le = w("moment().lang() is deprecated. Instead, use moment().localeData() to get the language configuration. Use moment().locale() to change languages.", function(a) {
        return void 0 === a ? this.localeData() : this.locale(a)
    });
    // FORMATTING
    T(0, ["gg", 2], 0, function() {
            return this.weekYear() % 100
        }), T(0, ["GG", 2], 0, function() {
            return this.isoWeekYear() % 100
        }), xc("gggg", "weekYear"), xc("ggggg", "weekYear"), xc("GGGG", "isoWeekYear"), xc("GGGGG", "isoWeekYear"),
        // ALIASES
        I("weekYear", "gg"), I("isoWeekYear", "GG"),
        // PRIORITY
        L("weekYear", 1), L("isoWeekYear", 1),
        // PARSING
        Y("G", Rd), Y("g", Rd), Y("GG", Kd, Gd), Y("gg", Kd, Gd), Y("GGGG", Od, Id), Y("gggg", Od, Id), Y("GGGGG", Pd, Jd), Y("ggggg", Pd, Jd), ba(["gggg", "ggggg", "GGGG", "GGGGG"], function(a, b, c, d) {
            b[d.substr(0, 2)] = t(a)
        }), ba(["gg", "GG"], function(b, c, d, e) {
            c[e] = a.parseTwoDigitYear(b)
        }),
        // FORMATTING
        T("Q", 0, "Qo", "quarter"),
        // ALIASES
        I("quarter", "Q"),
        // PRIORITY
        L("quarter", 7),
        // PARSING
        Y("Q", Fd), aa("Q", function(a, b) {
            b[Zd] = 3 * (t(a) - 1)
        }),
        // FORMATTING
        T("D", ["DD", 2], "Do", "date"),
        // ALIASES
        I("date", "D"),
        // PRIOROITY
        L("date", 9),
        // PARSING
        Y("D", Kd), Y("DD", Kd, Gd), Y("Do", function(a, b) {
            return a ? b._ordinalParse : b._ordinalParseLenient
        }), aa(["D", "DD"], $d), aa("Do", function(a, b) {
            b[$d] = t(a.match(Kd)[0], 10)
        });
    // MOMENTS
    var Me = N("Date", !0);
    // FORMATTING
    T("DDD", ["DDDD", 3], "DDDo", "dayOfYear"),
        // ALIASES
        I("dayOfYear", "DDD"),
        // PRIORITY
        L("dayOfYear", 4),
        // PARSING
        Y("DDD", Nd), Y("DDDD", Hd), aa(["DDD", "DDDD"], function(a, b, c) {
            c._dayOfYear = t(a)
        }),
        // FORMATTING
        T("m", ["mm", 2], 0, "minute"),
        // ALIASES
        I("minute", "m"),
        // PRIORITY
        L("minute", 14),
        // PARSING
        Y("m", Kd), Y("mm", Kd, Gd), aa(["m", "mm"], ae);
    // MOMENTS
    var Ne = N("Minutes", !1);
    // FORMATTING
    T("s", ["ss", 2], 0, "second"),
        // ALIASES
        I("second", "s"),
        // PRIORITY
        L("second", 15),
        // PARSING
        Y("s", Kd), Y("ss", Kd, Gd), aa(["s", "ss"], be);
    // MOMENTS
    var Oe = N("Seconds", !1);
    // FORMATTING
    T("S", 0, 0, function() {
            return ~~(this.millisecond() / 100)
        }), T(0, ["SS", 2], 0, function() {
            return ~~(this.millisecond() / 10)
        }), T(0, ["SSS", 3], 0, "millisecond"), T(0, ["SSSS", 4], 0, function() {
            return 10 * this.millisecond()
        }), T(0, ["SSSSS", 5], 0, function() {
            return 100 * this.millisecond()
        }), T(0, ["SSSSSS", 6], 0, function() {
            return 1e3 * this.millisecond()
        }), T(0, ["SSSSSSS", 7], 0, function() {
            return 1e4 * this.millisecond()
        }), T(0, ["SSSSSSSS", 8], 0, function() {
            return 1e5 * this.millisecond()
        }), T(0, ["SSSSSSSSS", 9], 0, function() {
            return 1e6 * this.millisecond()
        }),
        // ALIASES
        I("millisecond", "ms"),
        // PRIORITY
        L("millisecond", 16),
        // PARSING
        Y("S", Nd, Fd), Y("SS", Nd, Gd), Y("SSS", Nd, Hd);
    var Pe;
    for (Pe = "SSSS"; Pe.length <= 9; Pe += "S") Y(Pe, Qd);
    for (Pe = "S"; Pe.length <= 9; Pe += "S") aa(Pe, Gc);
    // MOMENTS
    var Qe = N("Milliseconds", !1);
    // FORMATTING
    T("z", 0, 0, "zoneAbbr"), T("zz", 0, 0, "zoneName");
    var Re = q.prototype;
    Re.add = Je, Re.calendar = Ub, Re.clone = Vb, Re.diff = ac, Re.endOf = mc, Re.format = ec, Re.from = fc, Re.fromNow = gc, Re.to = hc, Re.toNow = ic, Re.get = Q, Re.invalidAt = vc, Re.isAfter = Wb, Re.isBefore = Xb, Re.isBetween = Yb, Re.isSame = Zb, Re.isSameOrAfter = $b, Re.isSameOrBefore = _b, Re.isValid = tc, Re.lang = Le, Re.locale = jc, Re.localeData = kc, Re.max = Ee, Re.min = De, Re.parsingFlags = uc, Re.set = R, Re.startOf = lc, Re.subtract = Ke, Re.toArray = qc, Re.toObject = rc, Re.toDate = pc, Re.toISOString = dc, Re.toJSON = sc, Re.toString = cc, Re.unix = oc, Re.valueOf = nc, Re.creationData = wc,
        // Year
        Re.year = ke, Re.isLeapYear = qa,
        // Week Year
        Re.weekYear = yc, Re.isoWeekYear = zc,
        // Quarter
        Re.quarter = Re.quarters = Ec,
        // Month
        Re.month = ja, Re.daysInMonth = ka,
        // Week
        Re.week = Re.weeks = Aa, Re.isoWeek = Re.isoWeeks = Ba, Re.weeksInYear = Bc, Re.isoWeeksInYear = Ac,
        // Day
        Re.date = Me, Re.day = Re.days = Ja, Re.weekday = Ka, Re.isoWeekday = La, Re.dayOfYear = Fc,
        // Hour
        Re.hour = Re.hours = ue,
        // Minute
        Re.minute = Re.minutes = Ne,
        // Second
        Re.second = Re.seconds = Oe,
        // Millisecond
        Re.millisecond = Re.milliseconds = Qe,
        // Offset
        Re.utcOffset = Bb, Re.utc = Db, Re.local = Eb, Re.parseZone = Fb, Re.hasAlignedHourOffset = Gb, Re.isDST = Hb, Re.isLocal = Jb, Re.isUtcOffset = Kb, Re.isUtc = Lb, Re.isUTC = Lb,
        // Timezone
        Re.zoneAbbr = Hc, Re.zoneName = Ic,
        // Deprecations
        Re.dates = w("dates accessor is deprecated. Use date instead.", Me), Re.months = w("months accessor is deprecated. Use month instead", ja), Re.years = w("years accessor is deprecated. Use year instead", ke), Re.zone = w("moment().zone is deprecated, use moment().utcOffset instead. http://momentjs.com/guides/#/warnings/zone/", Cb), Re.isDSTShifted = w("isDSTShifted is deprecated. See http://momentjs.com/guides/#/warnings/dst-shifted/ for more information", Ib);
    var Se = Re,
        Te = B.prototype;
    Te.calendar = C, Te.longDateFormat = D, Te.invalidDate = E, Te.ordinal = F, Te.preparse = Lc, Te.postformat = Lc, Te.relativeTime = G, Te.pastFuture = H, Te.set = z,
        // Month
        Te.months = ea, Te.monthsShort = fa, Te.monthsParse = ha, Te.monthsRegex = ma, Te.monthsShortRegex = la,
        // Week
        Te.week = xa, Te.firstDayOfYear = za, Te.firstDayOfWeek = ya,
        // Day of Week
        Te.weekdays = Ea, Te.weekdaysMin = Ga, Te.weekdaysShort = Fa, Te.weekdaysParse = Ia, Te.weekdaysRegex = Ma, Te.weekdaysShortRegex = Na, Te.weekdaysMinRegex = Oa,
        // Hours
        Te.isPM = Ua, Te.meridiem = Va, Za("en", {
            ordinalParse: /\d{1,2}(th|st|nd|rd)/,
            ordinal: function(a) {
                var b = a % 10,
                    c = 1 === t(a % 100 / 10) ? "th" : 1 === b ? "st" : 2 === b ? "nd" : 3 === b ? "rd" : "th";
                return a + c
            }
        }),
        // Side effect imports
        a.lang = w("moment.lang is deprecated. Use moment.locale instead.", Za), a.langData = w("moment.langData is deprecated. Use moment.localeData instead.", ab);
    var Ue = Math.abs,
        Ve = cd("ms"),
        We = cd("s"),
        Xe = cd("m"),
        Ye = cd("h"),
        Ze = cd("d"),
        $e = cd("w"),
        _e = cd("M"),
        af = cd("y"),
        bf = ed("milliseconds"),
        cf = ed("seconds"),
        df = ed("minutes"),
        ef = ed("hours"),
        ff = ed("days"),
        gf = ed("months"),
        hf = ed("years"),
        jf = Math.round,
        kf = {
            s: 45, // seconds to minute
            m: 45, // minutes to hour
            h: 22, // hours to day
            d: 26, // days to month
            M: 11
        },
        lf = Math.abs,
        mf = vb.prototype;
    mf.abs = Uc, mf.add = Wc, mf.subtract = Xc, mf.as = ad, mf.asMilliseconds = Ve, mf.asSeconds = We, mf.asMinutes = Xe, mf.asHours = Ye, mf.asDays = Ze, mf.asWeeks = $e, mf.asMonths = _e, mf.asYears = af, mf.valueOf = bd, mf._bubble = Zc, mf.get = dd, mf.milliseconds = bf, mf.seconds = cf, mf.minutes = df, mf.hours = ef, mf.days = ff, mf.weeks = fd, mf.months = gf, mf.years = hf, mf.humanize = kd, mf.toISOString = ld, mf.toString = ld, mf.toJSON = ld, mf.locale = jc, mf.localeData = kc,
        // Deprecations
        mf.toIsoString = w("toIsoString() is deprecated. Please use toISOString() instead (notice the capitals)", ld), mf.lang = Le,
        // Side effect imports
        // FORMATTING
        T("X", 0, 0, "unix"), T("x", 0, 0, "valueOf"),
        // PARSING
        Y("x", Rd), Y("X", Ud), aa("X", function(a, b, c) {
            c._d = new Date(1e3 * parseFloat(a, 10))
        }), aa("x", function(a, b, c) {
            c._d = new Date(t(a))
        }),
        // Side effect imports
        a.version = "2.14.1", b(rb), a.fn = Se, a.min = tb, a.max = ub, a.now = Fe, a.utc = j, a.unix = Jc, a.months = Pc, a.isDate = f, a.locale = Za, a.invalid = n, a.duration = Mb, a.isMoment = r, a.weekdays = Rc, a.parseZone = Kc, a.localeData = ab, a.isDuration = wb, a.monthsShort = Qc, a.weekdaysMin = Tc, a.defineLocale = $a, a.updateLocale = _a, a.locales = bb, a.weekdaysShort = Sc, a.normalizeUnits = J, a.relativeTimeRounding = id, a.relativeTimeThreshold = jd, a.calendarFormat = Tb, a.prototype = Se;
    var nf = a;
    return nf
});
/* -------------- */
/*! version : 4.17.47
 =========================================================
 bootstrap-datetimejs
 https://github.com/Eonasdan/bootstrap-datetimepicker
 Copyright (c) 2015 Jonathan Peterson
 =========================================================
 */
/*
 The MIT License (MIT)

 Copyright (c) 2015 Jonathan Peterson

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 */
/*global define:false */
/*global exports:false */
/*global require:false */
/*global jQuery:false */
/*global moment:false */

/*


     Creative Tim Modifications

     We added class btn-primary for custom styling button.


*/

! function(e) {
  "use strict";
  if ("function" == typeof define && define.amd) define(["jquery", "moment"], e);
  else if ("object" == typeof exports) module.exports = e(require("jquery"), require("moment"));
  else {
    if ("undefined" == typeof jQuery) throw "bootstrap-datetimepicker requires jQuery to be loaded first";
    if ("undefined" == typeof moment) throw "bootstrap-datetimepicker requires Moment.js to be loaded first";
    e(jQuery, moment)
  }
}(function(e, t) {
  "use strict";
  if (!t) throw new Error("bootstrap-datetimepicker requires Moment.js to be loaded first");
  var n = function(n, a) {
    var r, i, o, s, d, l, p, c = {},
      u = !0,
      f = !1,
      h = !1,
      m = 0,
      y = [{
        clsName: "days",
        navFnc: "M",
        navStep: 1
      }, {
        clsName: "months",
        navFnc: "y",
        navStep: 1
      }, {
        clsName: "years",
        navFnc: "y",
        navStep: 10
      }, {
        clsName: "decades",
        navFnc: "y",
        navStep: 100
      }],
      b = ["days", "months", "years", "decades"],
      g = ["top", "bottom", "auto"],
      w = ["left", "right", "auto"],
      v = ["default", "top", "bottom"],
      k = {
        up: 38,
        38: "up",
        down: 40,
        40: "down",
        left: 37,
        37: "left",
        right: 39,
        39: "right",
        tab: 9,
        9: "tab",
        escape: 27,
        27: "escape",
        enter: 13,
        13: "enter",
        pageUp: 33,
        33: "pageUp",
        pageDown: 34,
        34: "pageDown",
        shift: 16,
        16: "shift",
        control: 17,
        17: "control",
        space: 32,
        32: "space",
        t: 84,
        84: "t",
        delete: 46,
        46: "delete"
      },
      D = {},
      C = function() {
        return void 0 !== t.tz && void 0 !== a.timeZone && null !== a.timeZone && "" !== a.timeZone
      },
      x = function(e) {
        var n;
        return n = void 0 === e || null === e ? t() : t.isDate(e) || t.isMoment(e) ? t(e) : C() ? t.tz(e, l, a.useStrict, a.timeZone) : t(e, l, a.useStrict), C() && n.tz(a.timeZone), n
      },
      T = function(e) {
        if ("string" != typeof e || e.length > 1) throw new TypeError("isEnabled expects a single character string parameter");
        switch (e) {
          case "y":
            return -1 !== d.indexOf("Y");
          case "M":
            return -1 !== d.indexOf("M");
          case "d":
            return -1 !== d.toLowerCase().indexOf("d");
          case "h":
          case "H":
            return -1 !== d.toLowerCase().indexOf("h");
          case "m":
            return -1 !== d.indexOf("m");
          case "s":
            return -1 !== d.indexOf("s");
          default:
            return !1
        }
      },
      M = function() {
        return T("h") || T("m") || T("s")
      },
      S = function() {
        return T("y") || T("M") || T("d")
      },
      O = function() {
        var t = e("<thead>").append(e("<tr>").append(e("<th>").addClass("prev").attr("data-action", "previous").append(e("<span>").addClass(a.icons.previous))).append(e("<th>").addClass("picker-switch").attr("data-action", "pickerSwitch").attr("colspan", a.calendarWeeks ? "6" : "5")).append(e("<th>").addClass("next").attr("data-action", "next").append(e("<span>").addClass(a.icons.next)))),
          n = e("<tbody>").append(e("<tr>").append(e("<td>").attr("colspan", a.calendarWeeks ? "8" : "7")));
        return [e("<div>").addClass("datepicker-days").append(e("<table>").addClass("table-condensed").append(t).append(e("<tbody>"))), e("<div>").addClass("datepicker-months").append(e("<table>").addClass("table-condensed").append(t.clone()).append(n.clone())), e("<div>").addClass("datepicker-years").append(e("<table>").addClass("table-condensed").append(t.clone()).append(n.clone())), e("<div>").addClass("datepicker-decades").append(e("<table>").addClass("table-condensed").append(t.clone()).append(n.clone()))]
      },
      P = function() {
        var t = e("<tr>"),
          n = e("<tr>"),
          r = e("<tr>");
        return T("h") && (t.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.incrementHour
        }).addClass("btn").attr("data-action", "incrementHours").append(e("<span>").addClass(a.icons.up)))), n.append(e("<td>").append(e("<span>").addClass("timepicker-hour").attr({
          "data-time-component": "hours",
          title: a.tooltips.pickHour
        }).attr("data-action", "showHours"))), r.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.decrementHour
        }).addClass("btn").attr("data-action", "decrementHours").append(e("<span>").addClass(a.icons.down))))), T("m") && (T("h") && (t.append(e("<td>").addClass("separator")), n.append(e("<td>").addClass("separator").html(":")), r.append(e("<td>").addClass("separator"))), t.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.incrementMinute
        }).addClass("btn").attr("data-action", "incrementMinutes").append(e("<span>").addClass(a.icons.up)))), n.append(e("<td>").append(e("<span>").addClass("timepicker-minute").attr({
          "data-time-component": "minutes",
          title: a.tooltips.pickMinute
        }).attr("data-action", "showMinutes"))), r.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.decrementMinute
        }).addClass("btn").attr("data-action", "decrementMinutes").append(e("<span>").addClass(a.icons.down))))), T("s") && (T("m") && (t.append(e("<td>").addClass("separator")), n.append(e("<td>").addClass("separator").html(":")), r.append(e("<td>").addClass("separator"))), t.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.incrementSecond
        }).addClass("btn btn-link").attr("data-action", "incrementSeconds").append(e("<span>").addClass(a.icons.up)))), n.append(e("<td>").append(e("<span>").addClass("timepicker-second").attr({
          "data-time-component": "seconds",
          title: a.tooltips.pickSecond
        }).attr("data-action", "showSeconds"))), r.append(e("<td>").append(e("<a>").attr({
          href: "#",
          tabindex: "-1",
          title: a.tooltips.decrementSecond
        }).addClass("btn btn-link").attr("data-action", "decrementSeconds").append(e("<span>").addClass(a.icons.down))))), s || (t.append(e("<td>").addClass("separator")), n.append(e("<td>").append(e("<button>").addClass("btn btn-primary").attr({
          "data-action": "togglePeriod",
          tabindex: "-1",
          title: a.tooltips.togglePeriod
        }))), r.append(e("<td>").addClass("separator"))), e("<div>").addClass("timepicker-picker").append(e("<table>").addClass("table-condensed").append([t, n, r]))
      },
      E = function() {
        var t = e("<div>").addClass("timepicker-hours").append(e("<table>").addClass("table-condensed")),
          n = e("<div>").addClass("timepicker-minutes").append(e("<table>").addClass("table-condensed")),
          a = e("<div>").addClass("timepicker-seconds").append(e("<table>").addClass("table-condensed")),
          r = [P()];
        return T("h") && r.push(t), T("m") && r.push(n), T("s") && r.push(a), r
      },
      H = function() {
        var t = [];
        return a.showTodayButton && t.push(e("<td>").append(e("<a>").attr({
          "data-action": "today",
          title: a.tooltips.today
        }).append(e("<span>").addClass(a.icons.today)))), !a.sideBySide && S() && M() && t.push(e("<td>").append(e("<a>").attr({
          "data-action": "togglePicker",
          title: a.tooltips.selectTime
        }).append(e("<span>").addClass(a.icons.time)))), a.showClear && t.push(e("<td>").append(e("<a>").attr({
          "data-action": "clear",
          title: a.tooltips.clear
        }).append(e("<span>").addClass(a.icons.clear)))), a.showClose && t.push(e("<td>").append(e("<a>").attr({
          "data-action": "close",
          title: a.tooltips.close
        }).append(e("<span>").addClass(a.icons.close)))), e("<table>").addClass("table-condensed").append(e("<tbody>").append(e("<tr>").append(t)))
      },
      I = function() {
        var t = e("<div>").addClass("bootstrap-datetimepicker-widget dropdown-menu"),
          n = e("<div>").addClass("datepicker").append(O()),
          r = e("<div>").addClass("timepicker").append(E()),
          i = e("<ul>").addClass("list-unstyled"),
          o = e("<li>").addClass("picker-switch" + (a.collapse ? " accordion-toggle" : "")).append(H());
        return a.inline && t.removeClass("dropdown-menu"), s && t.addClass("usetwentyfour"), T("s") && !s && t.addClass("wider"), a.sideBySide && S() && M() ? (t.addClass("timepicker-sbs"), "top" === a.toolbarPlacement && t.append(o), t.append(e("<div>").addClass("row").append(n.addClass("col-md-6")).append(r.addClass("col-md-6"))), "bottom" === a.toolbarPlacement && t.append(o), t) : ("top" === a.toolbarPlacement && i.append(o), S() && i.append(e("<li>").addClass(a.collapse && M() ? "collapse show" : "").append(n)), "default" === a.toolbarPlacement && i.append(o), M() && i.append(e("<li>").addClass(a.collapse && S() ? "collapse" : "").append(r)), "bottom" === a.toolbarPlacement && i.append(o), t.append(i))
      },
      Y = function() {
        var t, r = (f || n).position(),
          i = (f || n).offset(),
          o = a.widgetPositioning.vertical,
          s = a.widgetPositioning.horizontal;
        if (a.widgetParent) t = a.widgetParent.append(h);
        else if (n.is("input")) t = n.after(h).parent();
        else {
          if (a.inline) return void(t = n.append(h));
          t = n, n.children().first().after(h)
        }
        if ("auto" === o && (o = i.top + 1.5 * h.height() >= e(window).height() + e(window).scrollTop() && h.height() + n.outerHeight() < i.top ? "top" : "bottom"), "auto" === s && (s = t.width() < i.left + h.outerWidth() / 2 && i.left + h.outerWidth() > e(window).width() ? "right" : "left"), "top" === o ? h.addClass("top").removeClass("bottom") : h.addClass("bottom").removeClass("top"), "right" === s ? h.addClass("pull-right") : h.removeClass("pull-right"), "static" === t.css("position") && (t = t.parents().filter(function() {
            return "static" !== e(this).css("position")
          }).first()), 0 === t.length) throw new Error("datetimepicker component should be placed within a non-static positioned container");
        h.css({
          top: "top" === o ? "auto" : r.top + n.outerHeight(),
          bottom: "top" === o ? t.outerHeight() - (t === n ? 0 : r.top) : "auto",
          left: "left" === s ? t === n ? 0 : r.left : "auto",
          right: "left" === s ? "auto" : t.outerWidth() - n.outerWidth() - (t === n ? 0 : r.left)
        }), setTimeout(function() {
          h.addClass("open")
        }, 180)
      },
      q = function(e) {
        "dp.change" === e.type && (e.date && e.date.isSame(e.oldDate) || !e.date && !e.oldDate) || n.trigger(e)
      },
      B = function(e) {
        "y" === e && (e = "YYYY"), q({
          type: "dp.update",
          change: e,
          viewDate: i.clone()
        })
      },
      j = function(e) {
        h && (e && (p = Math.max(m, Math.min(3, p + e))), h.find(".datepicker > div").hide().filter(".datepicker-" + y[p].clsName).show())
      },
      A = function() {
        var t = e("<tr>"),
          n = i.clone().startOf("w").startOf("d");
        for (!0 === a.calendarWeeks && t.append(e("<th>").addClass("cw").text("#")); n.isBefore(i.clone().endOf("w"));) t.append(e("<th>").addClass("dow").text(n.format("dd"))), n.add(1, "d");
        h.find(".datepicker-days thead").append(t)
      },
      F = function(e) {
        return !0 === a.disabledDates[e.format("YYYY-MM-DD")]
      },
      L = function(e) {
        return !0 === a.enabledDates[e.format("YYYY-MM-DD")]
      },
      W = function(e) {
        return !0 === a.disabledHours[e.format("H")]
      },
      z = function(e) {
        return !0 === a.enabledHours[e.format("H")]
      },
      N = function(t, n) {
        if (!t.isValid()) return !1;
        if (a.disabledDates && "d" === n && F(t)) return !1;
        if (a.enabledDates && "d" === n && !L(t)) return !1;
        if (a.minDate && t.isBefore(a.minDate, n)) return !1;
        if (a.maxDate && t.isAfter(a.maxDate, n)) return !1;
        if (a.daysOfWeekDisabled && "d" === n && -1 !== a.daysOfWeekDisabled.indexOf(t.day())) return !1;
        if (a.disabledHours && ("h" === n || "m" === n || "s" === n) && W(t)) return !1;
        if (a.enabledHours && ("h" === n || "m" === n || "s" === n) && !z(t)) return !1;
        if (a.disabledTimeIntervals && ("h" === n || "m" === n || "s" === n)) {
          var r = !1;
          if (e.each(a.disabledTimeIntervals, function() {
              if (t.isBetween(this[0], this[1])) return r = !0, !1
            }), r) return !1
        }
        return !0
      },
      V = function() {
        for (var t = [], n = i.clone().startOf("y").startOf("d"); n.isSame(i, "y");) t.push(e("<span>").attr("data-action", "selectMonth").addClass("month").text(n.format("MMM"))), n.add(1, "M");
        h.find(".datepicker-months td").empty().append(t)
      },
      Z = function() {
        var t = h.find(".datepicker-months"),
          n = t.find("th"),
          o = t.find("tbody").find("span");
        n.eq(0).find("span").attr("title", a.tooltips.prevYear), n.eq(1).attr("title", a.tooltips.selectYear), n.eq(2).find("span").attr("title", a.tooltips.nextYear), t.find(".disabled").removeClass("disabled"), N(i.clone().subtract(1, "y"), "y") || n.eq(0).addClass("disabled"), n.eq(1).text(i.year()), N(i.clone().add(1, "y"), "y") || n.eq(2).addClass("disabled"), o.removeClass("active"), r.isSame(i, "y") && !u && o.eq(r.month()).addClass("active"), o.each(function(t) {
          N(i.clone().month(t), "M") || e(this).addClass("disabled")
        })
      },
      R = function() {
        var e = h.find(".datepicker-years"),
          t = e.find("th"),
          n = i.clone().subtract(5, "y"),
          o = i.clone().add(6, "y"),
          s = "";
        for (t.eq(0).find("span").attr("title", a.tooltips.prevDecade), t.eq(1).attr("title", a.tooltips.selectDecade), t.eq(2).find("span").attr("title", a.tooltips.nextDecade), e.find(".disabled").removeClass("disabled"), a.minDate && a.minDate.isAfter(n, "y") && t.eq(0).addClass("disabled"), t.eq(1).text(n.year() + "-" + o.year()), a.maxDate && a.maxDate.isBefore(o, "y") && t.eq(2).addClass("disabled"); !n.isAfter(o, "y");) s += '<span data-action="selectYear" class="year' + (n.isSame(r, "y") && !u ? " active" : "") + (N(n, "y") ? "" : " disabled") + '">' + n.year() + "</span>", n.add(1, "y");
        e.find("td").html(s)
      },
      Q = function() {
        var e, n = h.find(".datepicker-decades"),
          o = n.find("th"),
          s = t({
            y: i.year() - i.year() % 100 - 1
          }),
          d = s.clone().add(100, "y"),
          l = s.clone(),
          p = !1,
          c = !1,
          u = "";
        for (o.eq(0).find("span").attr("title", a.tooltips.prevCentury), o.eq(2).find("span").attr("title", a.tooltips.nextCentury), n.find(".disabled").removeClass("disabled"), (s.isSame(t({
            y: 1900
          })) || a.minDate && a.minDate.isAfter(s, "y")) && o.eq(0).addClass("disabled"), o.eq(1).text(s.year() + "-" + d.year()), (s.isSame(t({
            y: 2e3
          })) || a.maxDate && a.maxDate.isBefore(d, "y")) && o.eq(2).addClass("disabled"); !s.isAfter(d, "y");) e = s.year() + 12, p = a.minDate && a.minDate.isAfter(s, "y") && a.minDate.year() <= e, c = a.maxDate && a.maxDate.isAfter(s, "y") && a.maxDate.year() <= e, u += '<span data-action="selectDecade" class="decade' + (r.isAfter(s) && r.year() <= e ? " active" : "") + (N(s, "y") || p || c ? "" : " disabled") + '" data-selection="' + (s.year() + 6) + '">' + (s.year() + 1) + " - " + (s.year() + 12) + "</span>", s.add(12, "y");
        u += "<span></span><span></span><span></span>", n.find("td").html(u), o.eq(1).text(l.year() + 1 + "-" + s.year())
      },
      U = function() {
        var t, n, o, s = h.find(".datepicker-days"),
          d = s.find("th"),
          l = [],
          p = [];
        if (S()) {
          for (d.eq(0).find("span").attr("title", a.tooltips.prevMonth), d.eq(1).attr("title", a.tooltips.selectMonth), d.eq(2).find("span").attr("title", a.tooltips.nextMonth), s.find(".disabled").removeClass("disabled"), d.eq(1).text(i.format(a.dayViewHeaderFormat)), N(i.clone().subtract(1, "M"), "M") || d.eq(0).addClass("disabled"), N(i.clone().add(1, "M"), "M") || d.eq(2).addClass("disabled"), t = i.clone().startOf("M").startOf("w").startOf("d"), o = 0; o < 42; o++) 0 === t.weekday() && (n = e("<tr>"), a.calendarWeeks && n.append('<td class="cw">' + t.week() + "</td>"), l.push(n)), p = ["day"], t.isBefore(i, "M") && p.push("old"), t.isAfter(i, "M") && p.push("new"), t.isSame(r, "d") && !u && p.push("active"), N(t, "d") || p.push("disabled"), t.isSame(x(), "d") && p.push("today"), 0 !== t.day() && 6 !== t.day() || p.push("weekend"), q({
            type: "dp.classify",
            date: t,
            classNames: p
          }), n.append('<td data-action="selectDay" data-day="' + t.format("L") + '" class="' + p.join(" ") + '"><div>' + t.date() + "</div></td>"), t.add(1, "d");
          s.find("tbody").empty().append(l), Z(), R(), Q()
        }
      },
      G = function() {
        var t = h.find(".timepicker-hours table"),
          n = i.clone().startOf("d"),
          a = [],
          r = e("<tr>");
        for (i.hour() > 11 && !s && n.hour(12); n.isSame(i, "d") && (s || i.hour() < 12 && n.hour() < 12 || i.hour() > 11);) n.hour() % 4 == 0 && (r = e("<tr>"), a.push(r)), r.append('<td data-action="selectHour" class="hour' + (N(n, "h") ? "" : " disabled") + '"><div>' + n.format(s ? "HH" : "hh") + "</div></td>"), n.add(1, "h");
        t.empty().append(a)
      },
      J = function() {
        for (var t = h.find(".timepicker-minutes table"), n = i.clone().startOf("h"), r = [], o = e("<tr>"), s = 1 === a.stepping ? 5 : a.stepping; i.isSame(n, "h");) n.minute() % (4 * s) == 0 && (o = e("<tr>"), r.push(o)), o.append('<td data-action="selectMinute" class="minute' + (N(n, "m") ? "" : " disabled") + '"><div>' + n.format("mm") + "</div></td>"), n.add(s, "m");
        t.empty().append(r)
      },
      K = function() {
        for (var t = h.find(".timepicker-seconds table"), n = i.clone().startOf("m"), a = [], r = e("<tr>"); i.isSame(n, "m");) n.second() % 20 == 0 && (r = e("<tr>"), a.push(r)), r.append('<td data-action="selectSecond" class="second' + (N(n, "s") ? "" : " disabled") + '"><div>' + n.format("ss") + "</div></td>"), n.add(5, "s");
        t.empty().append(a)
      },
      X = function() {
        var e, t, n = h.find(".timepicker span[data-time-component]");
        s || (e = h.find(".timepicker [data-action=togglePeriod]"), t = r.clone().add(r.hours() >= 12 ? -12 : 12, "h"), e.text(r.format("A")), N(t, "h") ? e.removeClass("disabled") : e.addClass("disabled")), n.filter("[data-time-component=hours]").text(r.format(s ? "HH" : "hh")), n.filter("[data-time-component=minutes]").text(r.format("mm")), n.filter("[data-time-component=seconds]").text(r.format("ss")), G(), J(), K()
      },
      $ = function() {
        h && (U(), X())
      },
      _ = function(e) {
        var t = u ? null : r;
        if (!e) return u = !0, o.val(""), n.data("date", ""), q({
          type: "dp.change",
          date: !1,
          oldDate: t
        }), void $();
        if (e = e.clone().locale(a.locale), C() && e.tz(a.timeZone), 1 !== a.stepping)
          for (e.minutes(Math.round(e.minutes() / a.stepping) * a.stepping).seconds(0); a.minDate && e.isBefore(a.minDate);) e.add(a.stepping, "minutes");
        N(e) ? (i = (r = e).clone(), o.val(r.format(d)), n.data("date", r.format(d)), u = !1, $(), q({
          type: "dp.change",
          date: r.clone(),
          oldDate: t
        })) : (a.keepInvalid ? q({
          type: "dp.change",
          date: e,
          oldDate: t
        }) : o.val(u ? "" : r.format(d)), q({
          type: "dp.error",
          date: e,
          oldDate: t
        }))
      },
      ee = function() {
        var t = !1;
        return h ? (h.find(".collapse").each(function() {
          var n = e(this).data("collapse");
          return !n || !n.transitioning || (t = !0, !1)
        }), t ? c : (f && f.hasClass("btn") && f.toggleClass("active"), e(window).off("resize", Y), h.off("click", "[data-action]"), h.off("mousedown", !1), h.removeClass("open"), void setTimeout(function() {
          return h.remove(), h.hide(), h = !1, q({
            type: "dp.hide",
            date: r.clone()
          }), o.blur(), p = 0, i = r.clone(), c
        }, 400))) : c
      },
      te = function() {
        _(null)
      },
      ne = function(e) {
        return void 0 === a.parseInputDate ? (!t.isMoment(e) || e instanceof Date) && (e = x(e)) : e = a.parseInputDate(e), e
      },
      ae = {
        next: function() {
          var e = y[p].navFnc;
          i.add(y[p].navStep, e), U(), B(e)
        },
        previous: function() {
          var e = y[p].navFnc;
          i.subtract(y[p].navStep, e), U(), B(e)
        },
        pickerSwitch: function() {
          j(1)
        },
        selectMonth: function(t) {
          var n = e(t.target).closest("tbody").find("span").index(e(t.target));
          i.month(n), p === m ? (_(r.clone().year(i.year()).month(i.month())), a.inline || ee()) : (j(-1), U()), B("M")
        },
        selectYear: function(t) {
          var n = parseInt(e(t.target).text(), 10) || 0;
          i.year(n), p === m ? (_(r.clone().year(i.year())), a.inline || ee()) : (j(-1), U()), B("YYYY")
        },
        selectDecade: function(t) {
          var n = parseInt(e(t.target).data("selection"), 10) || 0;
          i.year(n), p === m ? (_(r.clone().year(i.year())), a.inline || ee()) : (j(-1), U()), B("YYYY")
        },
        selectDay: function(t) {
          var n = i.clone();
          e(t.target).is(".old") && n.subtract(1, "M"), e(t.target).is(".new") && n.add(1, "M"), _(n.date(parseInt(e(t.target).text(), 10))), M() || a.keepOpen || a.inline || ee()
        },
        incrementHours: function() {
          var e = r.clone().add(1, "h");
          N(e, "h") && _(e)
        },
        incrementMinutes: function() {
          var e = r.clone().add(a.stepping, "m");
          N(e, "m") && _(e)
        },
        incrementSeconds: function() {
          var e = r.clone().add(1, "s");
          N(e, "s") && _(e)
        },
        decrementHours: function() {
          var e = r.clone().subtract(1, "h");
          N(e, "h") && _(e)
        },
        decrementMinutes: function() {
          var e = r.clone().subtract(a.stepping, "m");
          N(e, "m") && _(e)
        },
        decrementSeconds: function() {
          var e = r.clone().subtract(1, "s");
          N(e, "s") && _(e)
        },
        togglePeriod: function() {
          _(r.clone().add(r.hours() >= 12 ? -12 : 12, "h"))
        },
        togglePicker: function(t) {
          var n, r = e(t.target),
            i = r.closest("ul"),
            o = i.find(".show"),
            s = i.find(".collapse:not(.show)");
          if (o && o.length) {
            if ((n = o.data("collapse")) && n.transitioning) return;
            o.collapse ? (o.collapse("hide"), s.collapse("show")) : (o.removeClass("show"), s.addClass("show")), r.is("span") ? r.toggleClass(a.icons.time + " " + a.icons.date) : r.find("span").toggleClass(a.icons.time + " " + a.icons.date)
          }
        },
        showPicker: function() {
          h.find(".timepicker > div:not(.timepicker-picker)").hide(), h.find(".timepicker .timepicker-picker").show()
        },
        showHours: function() {
          h.find(".timepicker .timepicker-picker").hide(), h.find(".timepicker .timepicker-hours").show()
        },
        showMinutes: function() {
          h.find(".timepicker .timepicker-picker").hide(), h.find(".timepicker .timepicker-minutes").show()
        },
        showSeconds: function() {
          h.find(".timepicker .timepicker-picker").hide(), h.find(".timepicker .timepicker-seconds").show()
        },
        selectHour: function(t) {
          var n = parseInt(e(t.target).text(), 10);
          s || (r.hours() >= 12 ? 12 !== n && (n += 12) : 12 === n && (n = 0)), _(r.clone().hours(n)), ae.showPicker.call(c)
        },
        selectMinute: function(t) {
          _(r.clone().minutes(parseInt(e(t.target).text(), 10))), ae.showPicker.call(c)
        },
        selectSecond: function(t) {
          _(r.clone().seconds(parseInt(e(t.target).text(), 10))), ae.showPicker.call(c)
        },
        clear: te,
        today: function() {
          var e = x();
          N(e, "d") && _(e)
        },
        close: ee
      },
      re = function(t) {
        return !e(t.currentTarget).is(".disabled") && (ae[e(t.currentTarget).data("action")].apply(c, arguments), !1)
      },
      ie = function() {
        var t, n = {
          year: function(e) {
            return e.month(0).date(1).hours(0).seconds(0).minutes(0)
          },
          month: function(e) {
            return e.date(1).hours(0).seconds(0).minutes(0)
          },
          day: function(e) {
            return e.hours(0).seconds(0).minutes(0)
          },
          hour: function(e) {
            return e.seconds(0).minutes(0)
          },
          minute: function(e) {
            return e.seconds(0)
          }
        };
        return o.prop("disabled") || !a.ignoreReadonly && o.prop("readonly") || h ? c : (void 0 !== o.val() && 0 !== o.val().trim().length ? _(ne(o.val().trim())) : u && a.useCurrent && (a.inline || o.is("input") && 0 === o.val().trim().length) && (t = x(), "string" == typeof a.useCurrent && (t = n[a.useCurrent](t)), _(t)), h = I(), A(), V(), h.find(".timepicker-hours").hide(), h.find(".timepicker-minutes").hide(), h.find(".timepicker-seconds").hide(), $(), j(), e(window).on("resize", Y), h.on("click", "[data-action]", re), h.on("mousedown", !1), f && f.hasClass("btn") && f.toggleClass("active"), Y(), h.show(), a.focusOnShow && !o.is(":focus") && o.focus(), q({
          type: "dp.show"
        }), c)
      },
      oe = function() {
        return h ? ee() : ie()
      },
      se = function(e) {
        var t, n, r, i, o = null,
          s = [],
          d = {},
          l = e.which;
        D[l] = "p";
        for (t in D) D.hasOwnProperty(t) && "p" === D[t] && (s.push(t), parseInt(t, 10) !== l && (d[t] = !0));
        for (t in a.keyBinds)
          if (a.keyBinds.hasOwnProperty(t) && "function" == typeof a.keyBinds[t] && (r = t.split(" ")).length === s.length && k[l] === r[r.length - 1]) {
            for (i = !0, n = r.length - 2; n >= 0; n--)
              if (!(k[r[n]] in d)) {
                i = !1;
                break
              }
            if (i) {
              o = a.keyBinds[t];
              break
            }
          }
        o && (o.call(c, h), e.stopPropagation(), e.preventDefault())
      },
      de = function(e) {
        D[e.which] = "r", e.stopPropagation(), e.preventDefault()
      },
      le = function(t) {
        var n = e(t.target).val().trim(),
          a = n ? ne(n) : null;
        return _(a), t.stopImmediatePropagation(), !1
      },
      pe = function() {
        o.off({
          change: le,
          blur: blur,
          keydown: se,
          keyup: de,
          focus: a.allowInputToggle ? ee : ""
        }), n.is("input") ? o.off({
          focus: ie
        }) : f && (f.off("click", oe), f.off("mousedown", !1))
      },
      ce = function(t) {
        var n = {};
        return e.each(t, function() {
          var e = ne(this);
          e.isValid() && (n[e.format("YYYY-MM-DD")] = !0)
        }), !!Object.keys(n).length && n
      },
      ue = function(t) {
        var n = {};
        return e.each(t, function() {
          n[this] = !0
        }), !!Object.keys(n).length && n
      },
      fe = function() {
        var e = a.format || "L LT";
        d = e.replace(/(\[[^\[]*\])|(\\)?(LTS|LT|LL?L?L?|l{1,4})/g, function(e) {
          return (r.localeData().longDateFormat(e) || e).replace(/(\[[^\[]*\])|(\\)?(LTS|LT|LL?L?L?|l{1,4})/g, function(e) {
            return r.localeData().longDateFormat(e) || e
          })
        }), (l = a.extraFormats ? a.extraFormats.slice() : []).indexOf(e) < 0 && l.indexOf(d) < 0 && l.push(d), s = d.toLowerCase().indexOf("a") < 1 && d.replace(/\[.*?\]/g, "").indexOf("h") < 1, T("y") && (m = 2), T("M") && (m = 1), T("d") && (m = 0), p = Math.max(m, p), u || _(r)
      };
    if (c.destroy = function() {
        ee(), pe(), n.removeData("DateTimePicker"), n.removeData("date")
      }, c.toggle = oe, c.show = ie, c.hide = ee, c.disable = function() {
        return ee(), f && f.hasClass("btn") && f.addClass("disabled"), o.prop("disabled", !0), c
      }, c.enable = function() {
        return f && f.hasClass("btn") && f.removeClass("disabled"), o.prop("disabled", !1), c
      }, c.ignoreReadonly = function(e) {
        if (0 === arguments.length) return a.ignoreReadonly;
        if ("boolean" != typeof e) throw new TypeError("ignoreReadonly () expects a boolean parameter");
        return a.ignoreReadonly = e, c
      }, c.options = function(t) {
        if (0 === arguments.length) return e.extend(!0, {}, a);
        if (!(t instanceof Object)) throw new TypeError("options() options parameter should be an object");
        return e.extend(!0, a, t), e.each(a, function(e, t) {
          if (void 0 === c[e]) throw new TypeError("option " + e + " is not recognized!");
          c[e](t)
        }), c
      }, c.date = function(e) {
        if (0 === arguments.length) return u ? null : r.clone();
        if (!(null === e || "string" == typeof e || t.isMoment(e) || e instanceof Date)) throw new TypeError("date() parameter must be one of [null, string, moment or Date]");
        return _(null === e ? null : ne(e)), c
      }, c.format = function(e) {
        if (0 === arguments.length) return a.format;
        if ("string" != typeof e && ("boolean" != typeof e || !1 !== e)) throw new TypeError("format() expects a string or boolean:false parameter " + e);
        return a.format = e, d && fe(), c
      }, c.timeZone = function(e) {
        if (0 === arguments.length) return a.timeZone;
        if ("string" != typeof e) throw new TypeError("newZone() expects a string parameter");
        return a.timeZone = e, c
      }, c.dayViewHeaderFormat = function(e) {
        if (0 === arguments.length) return a.dayViewHeaderFormat;
        if ("string" != typeof e) throw new TypeError("dayViewHeaderFormat() expects a string parameter");
        return a.dayViewHeaderFormat = e, c
      }, c.extraFormats = function(e) {
        if (0 === arguments.length) return a.extraFormats;
        if (!1 !== e && !(e instanceof Array)) throw new TypeError("extraFormats() expects an array or false parameter");
        return a.extraFormats = e, l && fe(), c
      }, c.disabledDates = function(t) {
        if (0 === arguments.length) return a.disabledDates ? e.extend({}, a.disabledDates) : a.disabledDates;
        if (!t) return a.disabledDates = !1, $(), c;
        if (!(t instanceof Array)) throw new TypeError("disabledDates() expects an array parameter");
        return a.disabledDates = ce(t), a.enabledDates = !1, $(), c
      }, c.enabledDates = function(t) {
        if (0 === arguments.length) return a.enabledDates ? e.extend({}, a.enabledDates) : a.enabledDates;
        if (!t) return a.enabledDates = !1, $(), c;
        if (!(t instanceof Array)) throw new TypeError("enabledDates() expects an array parameter");
        return a.enabledDates = ce(t), a.disabledDates = !1, $(), c
      }, c.daysOfWeekDisabled = function(e) {
        if (0 === arguments.length) return a.daysOfWeekDisabled.splice(0);
        if ("boolean" == typeof e && !e) return a.daysOfWeekDisabled = !1, $(), c;
        if (!(e instanceof Array)) throw new TypeError("daysOfWeekDisabled() expects an array parameter");
        if (a.daysOfWeekDisabled = e.reduce(function(e, t) {
            return (t = parseInt(t, 10)) > 6 || t < 0 || isNaN(t) ? e : (-1 === e.indexOf(t) && e.push(t), e)
          }, []).sort(), a.useCurrent && !a.keepInvalid) {
          for (var t = 0; !N(r, "d");) {
            if (r.add(1, "d"), 31 === t) throw "Tried 31 times to find a valid date";
            t++
          }
          _(r)
        }
        return $(), c
      }, c.maxDate = function(e) {
        if (0 === arguments.length) return a.maxDate ? a.maxDate.clone() : a.maxDate;
        if ("boolean" == typeof e && !1 === e) return a.maxDate = !1, $(), c;
        "string" == typeof e && ("now" !== e && "moment" !== e || (e = x()));
        var t = ne(e);
        if (!t.isValid()) throw new TypeError("maxDate() Could not parse date parameter: " + e);
        if (a.minDate && t.isBefore(a.minDate)) throw new TypeError("maxDate() date parameter is before options.minDate: " + t.format(d));
        return a.maxDate = t, a.useCurrent && !a.keepInvalid && r.isAfter(e) && _(a.maxDate), i.isAfter(t) && (i = t.clone().subtract(a.stepping, "m")), $(), c
      }, c.minDate = function(e) {
        if (0 === arguments.length) return a.minDate ? a.minDate.clone() : a.minDate;
        if ("boolean" == typeof e && !1 === e) return a.minDate = !1, $(), c;
        "string" == typeof e && ("now" !== e && "moment" !== e || (e = x()));
        var t = ne(e);
        if (!t.isValid()) throw new TypeError("minDate() Could not parse date parameter: " + e);
        if (a.maxDate && t.isAfter(a.maxDate)) throw new TypeError("minDate() date parameter is after options.maxDate: " + t.format(d));
        return a.minDate = t, a.useCurrent && !a.keepInvalid && r.isBefore(e) && _(a.minDate), i.isBefore(t) && (i = t.clone().add(a.stepping, "m")), $(), c
      }, c.defaultDate = function(e) {
        if (0 === arguments.length) return a.defaultDate ? a.defaultDate.clone() : a.defaultDate;
        if (!e) return a.defaultDate = !1, c;
        "string" == typeof e && (e = "now" === e || "moment" === e ? x() : x(e));
        var t = ne(e);
        if (!t.isValid()) throw new TypeError("defaultDate() Could not parse date parameter: " + e);
        if (!N(t)) throw new TypeError("defaultDate() date passed is invalid according to component setup validations");
        return a.defaultDate = t, (a.defaultDate && a.inline || "" === o.val().trim()) && _(a.defaultDate), c
      }, c.locale = function(e) {
        if (0 === arguments.length) return a.locale;
        if (!t.localeData(e)) throw new TypeError("locale() locale " + e + " is not loaded from moment locales!");
        return a.locale = e, r.locale(a.locale), i.locale(a.locale), d && fe(), h && (ee(), ie()), c
      }, c.stepping = function(e) {
        return 0 === arguments.length ? a.stepping : (e = parseInt(e, 10), (isNaN(e) || e < 1) && (e = 1), a.stepping = e, c)
      }, c.useCurrent = function(e) {
        var t = ["year", "month", "day", "hour", "minute"];
        if (0 === arguments.length) return a.useCurrent;
        if ("boolean" != typeof e && "string" != typeof e) throw new TypeError("useCurrent() expects a boolean or string parameter");
        if ("string" == typeof e && -1 === t.indexOf(e.toLowerCase())) throw new TypeError("useCurrent() expects a string parameter of " + t.join(", "));
        return a.useCurrent = e, c
      }, c.collapse = function(e) {
        if (0 === arguments.length) return a.collapse;
        if ("boolean" != typeof e) throw new TypeError("collapse() expects a boolean parameter");
        return a.collapse === e ? c : (a.collapse = e, h && (ee(), ie()), c)
      }, c.icons = function(t) {
        if (0 === arguments.length) return e.extend({}, a.icons);
        if (!(t instanceof Object)) throw new TypeError("icons() expects parameter to be an Object");
        return e.extend(a.icons, t), h && (ee(), ie()), c
      }, c.tooltips = function(t) {
        if (0 === arguments.length) return e.extend({}, a.tooltips);
        if (!(t instanceof Object)) throw new TypeError("tooltips() expects parameter to be an Object");
        return e.extend(a.tooltips, t), h && (ee(), ie()), c
      }, c.useStrict = function(e) {
        if (0 === arguments.length) return a.useStrict;
        if ("boolean" != typeof e) throw new TypeError("useStrict() expects a boolean parameter");
        return a.useStrict = e, c
      }, c.sideBySide = function(e) {
        if (0 === arguments.length) return a.sideBySide;
        if ("boolean" != typeof e) throw new TypeError("sideBySide() expects a boolean parameter");
        return a.sideBySide = e, h && (ee(), ie()), c
      }, c.viewMode = function(e) {
        if (0 === arguments.length) return a.viewMode;
        if ("string" != typeof e) throw new TypeError("viewMode() expects a string parameter");
        if (-1 === b.indexOf(e)) throw new TypeError("viewMode() parameter must be one of (" + b.join(", ") + ") value");
        return a.viewMode = e, p = Math.max(b.indexOf(e), m), j(), c
      }, c.toolbarPlacement = function(e) {
        if (0 === arguments.length) return a.toolbarPlacement;
        if ("string" != typeof e) throw new TypeError("toolbarPlacement() expects a string parameter");
        if (-1 === v.indexOf(e)) throw new TypeError("toolbarPlacement() parameter must be one of (" + v.join(", ") + ") value");
        return a.toolbarPlacement = e, h && (ee(), ie()), c
      }, c.widgetPositioning = function(t) {
        if (0 === arguments.length) return e.extend({}, a.widgetPositioning);
        if ("[object Object]" !== {}.toString.call(t)) throw new TypeError("widgetPositioning() expects an object variable");
        if (t.horizontal) {
          if ("string" != typeof t.horizontal) throw new TypeError("widgetPositioning() horizontal variable must be a string");
          if (t.horizontal = t.horizontal.toLowerCase(), -1 === w.indexOf(t.horizontal)) throw new TypeError("widgetPositioning() expects horizontal parameter to be one of (" + w.join(", ") + ")");
          a.widgetPositioning.horizontal = t.horizontal
        }
        if (t.vertical) {
          if ("string" != typeof t.vertical) throw new TypeError("widgetPositioning() vertical variable must be a string");
          if (t.vertical = t.vertical.toLowerCase(), -1 === g.indexOf(t.vertical)) throw new TypeError("widgetPositioning() expects vertical parameter to be one of (" + g.join(", ") + ")");
          a.widgetPositioning.vertical = t.vertical
        }
        return $(), c
      }, c.calendarWeeks = function(e) {
        if (0 === arguments.length) return a.calendarWeeks;
        if ("boolean" != typeof e) throw new TypeError("calendarWeeks() expects parameter to be a boolean value");
        return a.calendarWeeks = e, $(), c
      }, c.showTodayButton = function(e) {
        if (0 === arguments.length) return a.showTodayButton;
        if ("boolean" != typeof e) throw new TypeError("showTodayButton() expects a boolean parameter");
        return a.showTodayButton = e, h && (ee(), ie()), c
      }, c.showClear = function(e) {
        if (0 === arguments.length) return a.showClear;
        if ("boolean" != typeof e) throw new TypeError("showClear() expects a boolean parameter");
        return a.showClear = e, h && (ee(), ie()), c
      }, c.widgetParent = function(t) {
        if (0 === arguments.length) return a.widgetParent;
        if ("string" == typeof t && (t = e(t)), null !== t && "string" != typeof t && !(t instanceof e)) throw new TypeError("widgetParent() expects a string or a jQuery object parameter");
        return a.widgetParent = t, h && (ee(), ie()), c
      }, c.keepOpen = function(e) {
        if (0 === arguments.length) return a.keepOpen;
        if ("boolean" != typeof e) throw new TypeError("keepOpen() expects a boolean parameter");
        return a.keepOpen = e, c
      }, c.focusOnShow = function(e) {
        if (0 === arguments.length) return a.focusOnShow;
        if ("boolean" != typeof e) throw new TypeError("focusOnShow() expects a boolean parameter");
        return a.focusOnShow = e, c
      }, c.inline = function(e) {
        if (0 === arguments.length) return a.inline;
        if ("boolean" != typeof e) throw new TypeError("inline() expects a boolean parameter");
        return a.inline = e, c
      }, c.clear = function() {
        return te(), c
      }, c.keyBinds = function(e) {
        return 0 === arguments.length ? a.keyBinds : (a.keyBinds = e, c)
      }, c.getMoment = function(e) {
        return x(e)
      }, c.debug = function(e) {
        if ("boolean" != typeof e) throw new TypeError("debug() expects a boolean parameter");
        return a.debug = e, c
      }, c.allowInputToggle = function(e) {
        if (0 === arguments.length) return a.allowInputToggle;
        if ("boolean" != typeof e) throw new TypeError("allowInputToggle() expects a boolean parameter");
        return a.allowInputToggle = e, c
      }, c.showClose = function(e) {
        if (0 === arguments.length) return a.showClose;
        if ("boolean" != typeof e) throw new TypeError("showClose() expects a boolean parameter");
        return a.showClose = e, c
      }, c.keepInvalid = function(e) {
        if (0 === arguments.length) return a.keepInvalid;
        if ("boolean" != typeof e) throw new TypeError("keepInvalid() expects a boolean parameter");
        return a.keepInvalid = e, c
      }, c.datepickerInput = function(e) {
        if (0 === arguments.length) return a.datepickerInput;
        if ("string" != typeof e) throw new TypeError("datepickerInput() expects a string parameter");
        return a.datepickerInput = e, c
      }, c.parseInputDate = function(e) {
        if (0 === arguments.length) return a.parseInputDate;
        if ("function" != typeof e) throw new TypeError("parseInputDate() sholud be as function");
        return a.parseInputDate = e, c
      }, c.disabledTimeIntervals = function(t) {
        if (0 === arguments.length) return a.disabledTimeIntervals ? e.extend({}, a.disabledTimeIntervals) : a.disabledTimeIntervals;
        if (!t) return a.disabledTimeIntervals = !1, $(), c;
        if (!(t instanceof Array)) throw new TypeError("disabledTimeIntervals() expects an array parameter");
        return a.disabledTimeIntervals = t, $(), c
      }, c.disabledHours = function(t) {
        if (0 === arguments.length) return a.disabledHours ? e.extend({}, a.disabledHours) : a.disabledHours;
        if (!t) return a.disabledHours = !1, $(), c;
        if (!(t instanceof Array)) throw new TypeError("disabledHours() expects an array parameter");
        if (a.disabledHours = ue(t), a.enabledHours = !1, a.useCurrent && !a.keepInvalid) {
          for (var n = 0; !N(r, "h");) {
            if (r.add(1, "h"), 24 === n) throw "Tried 24 times to find a valid date";
            n++
          }
          _(r)
        }
        return $(), c
      }, c.enabledHours = function(t) {
        if (0 === arguments.length) return a.enabledHours ? e.extend({}, a.enabledHours) : a.enabledHours;
        if (!t) return a.enabledHours = !1, $(), c;
        if (!(t instanceof Array)) throw new TypeError("enabledHours() expects an array parameter");
        if (a.enabledHours = ue(t), a.disabledHours = !1, a.useCurrent && !a.keepInvalid) {
          for (var n = 0; !N(r, "h");) {
            if (r.add(1, "h"), 24 === n) throw "Tried 24 times to find a valid date";
            n++
          }
          _(r)
        }
        return $(), c
      }, c.viewDate = function(e) {
        if (0 === arguments.length) return i.clone();
        if (!e) return i = r.clone(), c;
        if (!("string" == typeof e || t.isMoment(e) || e instanceof Date)) throw new TypeError("viewDate() parameter must be one of [string, moment or Date]");
        return i = ne(e), B(), c
      }, n.is("input")) o = n;
    else if (0 === (o = n.find(a.datepickerInput)).length) o = n.find("input");
    else if (!o.is("input")) throw new Error('CSS class "' + a.datepickerInput + '" cannot be applied to non input element');
    if (n.hasClass("input-group") && (f = 0 === n.find(".datepickerbutton").length ? n.find(".input-group-addon") : n.find(".datepickerbutton")), !a.inline && !o.is("input")) throw new Error("Could not initialize DateTimePicker without an input element");
    return r = x(), i = r.clone(), e.extend(!0, a, function() {
      var t, r = {};
      return (t = n.is("input") || a.inline ? n.data() : n.find("input").data()).dateOptions && t.dateOptions instanceof Object && (r = e.extend(!0, r, t.dateOptions)), e.each(a, function(e) {
        var n = "date" + e.charAt(0).toUpperCase() + e.slice(1);
        void 0 !== t[n] && (r[e] = t[n])
      }), r
    }()), c.options(a), fe(), o.on({
      change: le,
      blur: a.debug ? "" : ee,
      keydown: se,
      keyup: de,
      focus: a.allowInputToggle ? ie : ""
    }), n.is("input") ? o.on({
      focus: ie
    }) : f && (f.on("click", oe), f.on("mousedown", !1)), o.prop("disabled") && c.disable(), o.is("input") && 0 !== o.val().trim().length ? _(ne(o.val().trim())) : a.defaultDate && void 0 === o.attr("placeholder") && _(a.defaultDate), a.inline && ie(), c
  };
  return e.fn.datetimepicker = function(t) {
    t = t || {};
    var a, r = Array.prototype.slice.call(arguments, 1),
      i = !0,
      o = ["destroy", "hide", "show", "toggle"];
    if ("object" == typeof t) return this.each(function() {
      var a, r = e(this);
      r.data("DateTimePicker") || (a = e.extend(!0, {}, e.fn.datetimepicker.defaults, t), r.data("DateTimePicker", n(r, a)))
    });
    if ("string" == typeof t) return this.each(function() {
      var n = e(this).data("DateTimePicker");
      if (!n) throw new Error('bootstrap-datetimepicker("' + t + '") method was called on an element that is not using DateTimePicker');
      a = n[t].apply(n, r), i = a === n
    }), i || e.inArray(t, o) > -1 ? this : a;
    throw new TypeError("Invalid arguments for DateTimePicker: " + t)
  }, e.fn.datetimepicker.defaults = {
    timeZone: "",
    format: !1,
    dayViewHeaderFormat: "MMMM YYYY",
    extraFormats: !1,
    stepping: 1,
    minDate: !1,
    maxDate: !1,
    useCurrent: !0,
    collapse: !0,
    locale: t.locale(),
    defaultDate: !1,
    disabledDates: !1,
    enabledDates: !1,
    icons: {
      time: "glyphicon glyphicon-time",
      date: "glyphicon glyphicon-calendar",
      up: "glyphicon glyphicon-chevron-up",
      down: "glyphicon glyphicon-chevron-down",
      previous: "glyphicon glyphicon-chevron-left",
      next: "glyphicon glyphicon-chevron-right",
      today: "glyphicon glyphicon-screenshot",
      clear: "glyphicon glyphicon-trash",
      close: "glyphicon glyphicon-remove"
    },
    tooltips: {
      today: "Go to today",
      clear: "Clear selection",
      close: "Close the picker",
      selectMonth: "Select Month",
      prevMonth: "Previous Month",
      nextMonth: "Next Month",
      selectYear: "Select Year",
      prevYear: "Previous Year",
      nextYear: "Next Year",
      selectDecade: "Select Decade",
      prevDecade: "Previous Decade",
      nextDecade: "Next Decade",
      prevCentury: "Previous Century",
      nextCentury: "Next Century",
      pickHour: "Pick Hour",
      incrementHour: "Increment Hour",
      decrementHour: "Decrement Hour",
      pickMinute: "Pick Minute",
      incrementMinute: "Increment Minute",
      decrementMinute: "Decrement Minute",
      pickSecond: "Pick Second",
      incrementSecond: "Increment Second",
      decrementSecond: "Decrement Second",
      togglePeriod: "Toggle Period",
      selectTime: "Select Time"
    },
    useStrict: !1,
    sideBySide: !1,
    daysOfWeekDisabled: !1,
    calendarWeeks: !1,
    viewMode: "days",
    toolbarPlacement: "default",
    showTodayButton: !1,
    showClear: !1,
    showClose: !1,
    widgetPositioning: {
      horizontal: "auto",
      vertical: "auto"
    },
    widgetParent: null,
    ignoreReadonly: !1,
    keepOpen: !1,
    focusOnShow: !0,
    inline: !1,
    keepInvalid: !1,
    datepickerInput: ".datepickerinput",
    keyBinds: {
      up: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") ? this.date(t.clone().subtract(7, "d")) : this.date(t.clone().add(this.stepping(), "m"))
        }
      },
      down: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") ? this.date(t.clone().add(7, "d")) : this.date(t.clone().subtract(this.stepping(), "m"))
        } else this.show()
      },
      "control up": function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") ? this.date(t.clone().subtract(1, "y")) : this.date(t.clone().add(1, "h"))
        }
      },
      "control down": function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") ? this.date(t.clone().add(1, "y")) : this.date(t.clone().subtract(1, "h"))
        }
      },
      left: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") && this.date(t.clone().subtract(1, "d"))
        }
      },
      right: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") && this.date(t.clone().add(1, "d"))
        }
      },
      pageUp: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") && this.date(t.clone().subtract(1, "M"))
        }
      },
      pageDown: function(e) {
        if (e) {
          var t = this.date() || this.getMoment();
          e.find(".datepicker").is(":visible") && this.date(t.clone().add(1, "M"))
        }
      },
      enter: function() {
        this.hide()
      },
      escape: function() {
        this.hide()
      },
      "control space": function(e) {
        e && e.find(".timepicker").is(":visible") && e.find('.btn[data-action="togglePeriod"]').click()
      },
      t: function() {
        this.date(this.getMoment())
      },
      delete: function() {
        this.clear()
      }
    },
    debug: !1,
    allowInputToggle: !1,
    disabledTimeIntervals: !1,
    disabledHours: !1,
    enabledHours: !1,
    viewDate: !1
  }, e.fn.datetimepicker
});