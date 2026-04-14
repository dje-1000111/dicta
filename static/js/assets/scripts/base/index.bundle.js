/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/scripts/base/cookie_consent.js":
/*!***********************************************!*\
  !*** ./assets/scripts/base/cookie_consent.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   consentApp: () => (/* binding */ consentApp),\n/* harmony export */   getCookie: () => (/* binding */ getCookie)\n/* harmony export */ });\nconst cookieStorage = {\r\n    setItem: (item, value) => {\r\n        document.cookie = `${item}=${value}; path=/`\r\n    },\r\n}\r\n\r\nconst storageType = cookieStorage\r\nconst consentPropertyName = \"DT_CONSENT\"\r\n\r\nconst shouldShowPopup = () => !storageType.getItem(consentPropertyName)\r\nconst saveToStorage = () => storageType.setItem(consentPropertyName, true)\r\n\r\nfunction getCookie(name) {\r\n    const value = `; ${document.cookie}`;\r\n    const parts = value.split(`; ${name}=`);\r\n    if (parts.length === 2) return parts.pop().split(';').shift();\r\n}\r\n\r\nfunction createCookieConsentContainer() {\r\n    let div = document.getElementById(\"consent-popup\")\r\n    div.className = \"cookies-consent-container position-fixed bottom-2 end-2 p-4 rounded\"\r\n    if (getCookie(consentPropertyName)) {\r\n        div.remove()\r\n    } else {\r\n        var h4 = document.createElement(\"h4\")\r\n        h4.className = \"cookies-consent-title mb-2 text-xl\"\r\n        let h4Content = document.createTextNode(\"Cookies consent\")\r\n        h4.appendChild(h4Content)\r\n        div.appendChild(h4)\r\n        let p = document.createElement(\"p\")\r\n        p.className = \"cookies-consent-info mb-4\"\r\n        let pContent = document.createTextNode(\"By using our website, you automatically accept that we use cookies.\")\r\n        p.appendChild(pContent)\r\n        div.appendChild(p)\r\n\r\n        let btnConsentAll = document.createElement(\"button\")\r\n        btnConsentAll.id = \"btn-consent-all\"\r\n        btnConsentAll.className = \"btn btn-secondary btn-sm\"\r\n        btnConsentAll.type = \"submit\"\r\n        let btnConsentAllContent = document.createTextNode(\"Accept all\")\r\n        btnConsentAll.appendChild(btnConsentAllContent)\r\n        div.appendChild(btnConsentAll)\r\n\r\n        let btnConsentMinimal = document.createElement(\"button\")\r\n        btnConsentMinimal.id = \"btn-consent-minimal\"\r\n        btnConsentMinimal.className = \"btn btn-secondary btn-sm ms-2\"\r\n        btnConsentMinimal.type = \"submit\"\r\n        let btnConsentMinimalContent = document.createTextNode(\"Accept Selection\")\r\n        btnConsentMinimal.appendChild(btnConsentMinimalContent)\r\n        div.appendChild(btnConsentMinimal)\r\n\r\n        let divOptions = document.createElement(\"div\")\r\n        divOptions.className = \"mt-3\"\r\n\r\n        let labelAll = document.createElement(\"label\")\r\n        labelAll.className = \"me-3\"\r\n        let labelAllContent = document.createTextNode(\"Necessary\")\r\n        labelAll.appendChild(labelAllContent)\r\n        let inputNecessary = document.createElement(\"input\")\r\n        inputNecessary.setAttribute(\"type\", \"checkbox\");\r\n        inputNecessary.setAttribute(\"value\", \"necessary\");\r\n        inputNecessary.setAttribute(\"checked\", \"checked\");\r\n        inputNecessary.setAttribute(\"disabled\", \"disabled\");\r\n        inputNecessary.className = \"input-consent\"\r\n        divOptions.appendChild(labelAll)\r\n        labelAll.appendChild(inputNecessary)\r\n        div.appendChild(divOptions)\r\n\r\n        let labelSel = document.createElement(\"label\")\r\n        let labelSelContent = document.createTextNode(\"Analytics\")\r\n        labelSel.appendChild(labelSelContent)\r\n        let inputSelection = document.createElement(\"input\")\r\n        inputSelection.setAttribute(\"type\", \"checkbox\");\r\n        inputSelection.setAttribute(\"value\", \"analytics\");\r\n        inputSelection.setAttribute(\"checked\", \"checked\");\r\n        inputSelection.className = \"input-consent\"\r\n        inputSelection.id = \"ga\"\r\n        divOptions.appendChild(labelSel)\r\n        labelSel.appendChild(inputSelection)\r\n        div.appendChild(divOptions)\r\n\r\n    }\r\n}\r\nif (!getCookie(consentPropertyName) || localStorage.getItem('consentMode') === null) createCookieConsentContainer()\r\n\r\nconst consentPopup = document.getElementById(\"consent-popup\")\r\nconst consentAll = document.getElementById(\"btn-consent-all\")\r\nconst consentMinimal = document.getElementById(\"btn-consent-minimal\")\r\n\r\nfunction consentApp() {\r\n    saveToStorage(storageType);\r\n    createCookieConsentContainer()\r\n}\r\n\r\nif (localStorage.getItem('consentMode') === null || !getCookie(consentPropertyName)) {\r\n    if (consentAll) consentAll.addEventListener('click', function () {\r\n        consentApp()\r\n        setConsent({\r\n            necessary: true,\r\n            analytics: true,\r\n        });\r\n    });\r\n    if (consentMinimal) consentMinimal.addEventListener('click', function () {\r\n        consentApp()\r\n        setConsent({\r\n            necessary: true,\r\n            analytics: false,\r\n        });\r\n    });\r\n}\r\n\r\nfunction setConsent(consent) {\r\n    const consentMode = {\r\n        'functionality_storage': consent.necessary ? 'granted' : 'denied',\r\n        'security_storage': consent.necessary ? 'granted' : 'denied',\r\n        'ad_storage': consent.marketing ? 'granted' : 'denied',\r\n        'analytics_storage': consent.analytics ? 'granted' : 'denied',\r\n        'personalization': consent.preferences ? 'granted' : 'denied',\r\n    };\r\n    gtag('consent', 'update', consentMode);\r\n    localStorage.setItem('consentMode', JSON.stringify(consentMode));\r\n}\n\n//# sourceURL=webpack://dictatube/./assets/scripts/base/cookie_consent.js?");

/***/ }),

/***/ "./assets/scripts/base/index.js":
/*!**************************************!*\
  !*** ./assets/scripts/base/index.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _toggle_mode__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./toggle_mode */ \"./assets/scripts/base/toggle_mode.js\");\n/* harmony import */ var _toggle_mode__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_toggle_mode__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _cookie_consent__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./cookie_consent */ \"./assets/scripts/base/cookie_consent.js\");\n\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/base/index.js?");

/***/ }),

/***/ "./assets/scripts/base/toggle_mode.js":
/*!********************************************!*\
  !*** ./assets/scripts/base/toggle_mode.js ***!
  \********************************************/
/***/ (() => {

eval("const ligbtn = document.getElementById(\"ligbtn\")\r\nconst darkBtn = document.getElementById(\"darkbtn\")\r\n\r\nvar darkMode;\r\nif (localStorage.getItem('dark-mode')) {\r\n    darkMode = localStorage.getItem('dark-mode');\r\n} else {\r\n    darkMode = 'light';\r\n}\r\nlocalStorage.setItem('dark-mode', darkMode);\r\n\r\nvar tables = document.querySelectorAll(\"table\")\r\nvar tableLinks = document.querySelectorAll(\"table a.link-wrap\")\r\n\r\nif (document.getElementById(\"hcontainer\")) {\r\n    var hcontainer = document.getElementById(\"hcontainer\")\r\n}\r\n\r\nif (document.getElementById(\"tcontainer\")) {\r\n    var tcontainer = document.getElementById(\"tcontainer\")\r\n}\r\n\r\nif (document.getElementById(\"embvid\")) {\r\n    var embvid = document.getElementById(\"embvid\")\r\n}\r\n\r\nif (document.getElementById(\"text-area\")) {\r\n    var textarea = document.getElementById(\"text-area\")\r\n}\r\n\r\nif (document.getElementById(\"subh\")) {\r\n    var subh = document.getElementById(\"subh\")\r\n}\r\n\r\nif (document.getElementById(\"bonus-txt\")) {\r\n    var bonusTxt = document.getElementById(\"bonus-txt\")\r\n}\r\n\r\nif (document.getElementById(\"bonus-container\")) {\r\n    var bonusContainer = document.getElementById(\"bonus-container\")\r\n}\r\n\r\nif (document.getElementById(\"prof\")) {\r\n    var prof = document.getElementById(\"prof\")\r\n}\r\n\r\nif (document.getElementById(\"profile-container\")) {\r\n    var profileContainer = document.getElementById(\"profile-container\")\r\n}\r\n\r\nif (document.querySelector(\"main\")) {\r\n    var main = document.querySelector(\"main\")\r\n}\r\n\r\nif (document.getElementById(\"counter-cont\")) {\r\n    var counterCont = document.getElementById(\"counter-cont\")\r\n}\r\n\r\nif (document.getElementById(\"lab\")) {\r\n    var lab = document.getElementById(\"lab\")\r\n}\r\n\r\nif (document.querySelector(\"#lab a\")) {\r\n    var labA = document.querySelector(\"#lab a\")\r\n}\r\n\r\nif (document.getElementById(\"about\")) {\r\n    var about = document.getElementById(\"about\")\r\n}\r\n\r\nif (document.querySelector(\"#about a\")) {\r\n    var aboutA = document.querySelector(\"#about a\")\r\n}\r\n\r\nif (document.getElementById(\"toggle\")) {\r\n    var toggle = document.getElementById(\"toggle\")\r\n}\r\n\r\nvar achA = document.querySelectorAll(\"#ach a\")\r\n\r\nif (localStorage.getItem('dark-mode') == 'dark') {\r\n    if (hcontainer) {\r\n        hcontainer.classList.toggle(\"dark-mode\");\r\n        hcontainer.classList.add(\"hdark\");\r\n\r\n        for (const item of tableLinks) {\r\n            item.classList.add(\"link-light\");\r\n            item.classList.remove(\"link-primary\");\r\n        }\r\n    }\r\n    if (tcontainer) {\r\n        tcontainer.classList.toggle(\"dark-mode\");\r\n    }\r\n\r\n    if (lab) {\r\n        lab.classList.add(\"dark-lab-cont\");\r\n        lab.classList.remove(\"light-lab-cont\");\r\n    }\r\n\r\n    if (about) {\r\n        about.classList.add(\"dark-about-cont\");\r\n        about.classList.remove(\"light-about-cont\");\r\n\r\n        aboutA.classList.add(\"link-light\");\r\n        aboutA.classList.remove(\"link-primary\");\r\n    }\r\n\r\n    if (subh) {\r\n        subh.classList.add(\"dark\");\r\n        subh.classList.remove(\"light\");\r\n\r\n        embvid.classList.add(\"dark\");\r\n        embvid.classList.remove(\"light\");\r\n        textarea.classList.add(\"dark\");\r\n        textarea.classList.remove(\"light\");\r\n        bonusTxt.classList.add(\"dark\");\r\n        bonusTxt.classList.remove(\"light\");\r\n\r\n        bonusContainer.classList.add(\"dark-bonus-cont\");\r\n        bonusContainer.classList.remove(\"light-bonus-cont\");\r\n\r\n        counterCont.classList.add(\"dark-counter-cont\");\r\n        counterCont.classList.remove(\"light-counter-cont\");\r\n\r\n    }\r\n\r\n    if (achA) {\r\n        achA.forEach(item => {\r\n            item.classList.add(\"link-light\");\r\n            item.classList.remove(\"link-primary\");\r\n        });\r\n    }\r\n\r\n    if (main) {\r\n        main.classList.add(\"dark\");\r\n        main.classList.remove(\"light\");\r\n    }\r\n\r\n    if (prof) {\r\n        profileContainer.classList.add(\"dark-profile-cont\");\r\n        profileContainer.classList.remove(\"light-profile-cont\");\r\n    }\r\n\r\n    if (toggle) {\r\n        toggle.classList.add(\"link-light\");\r\n        toggle.classList.remove(\"link-primary\");\r\n    }\r\n\r\n    darkBtn.hidden = true\r\n    ligbtn.hidden = false\r\n    tables.forEach(table => {\r\n        table.classList.add(\"table-dark\")\r\n    });\r\n}\r\n\r\ndarkBtn.addEventListener(\"click\", function (e) {\r\n    if (e.target.hidden === false) {\r\n        darkBtn.hidden = true\r\n        ligbtn.hidden = false\r\n        if (hcontainer) {\r\n            hcontainer.classList.toggle(\"dark-mode\");\r\n            hcontainer.classList.add(\"hdark\");\r\n\r\n            for (const item of tableLinks) {\r\n                item.classList.add(\"link-light\");\r\n                item.classList.remove(\"link-primary\");\r\n            }\r\n        }\r\n\r\n        if (lab) {\r\n            lab.classList.add(\"dark-lab-cont\");\r\n            lab.classList.remove(\"light-lab-cont\");\r\n        }\r\n\r\n        if (about) {\r\n            about.classList.add(\"dark-about-cont\");\r\n            about.classList.remove(\"light-about-cont\");\r\n            aboutA.classList.add(\"link-light\");\r\n            aboutA.classList.remove(\"link-primary\");\r\n        }\r\n\r\n        if (tcontainer) {\r\n            tcontainer.classList.toggle(\"dark-mode\");\r\n        }\r\n        if (subh) {\r\n            subh.classList.add(\"dark\");\r\n            subh.classList.remove(\"light\");\r\n            embvid.classList.add(\"dark\");\r\n            embvid.classList.remove(\"light\");\r\n            textarea.classList.add(\"dark\");\r\n            textarea.classList.remove(\"light\");\r\n            bonusTxt.classList.add(\"dark\");\r\n            bonusTxt.classList.remove(\"light\");\r\n\r\n            bonusContainer.classList.add(\"dark-bonus-cont\");\r\n            bonusContainer.classList.remove(\"light-bonus-cont\");\r\n            counterCont.classList.add(\"dark-counter-cont\");\r\n            counterCont.classList.remove(\"light-counter-cont\");\r\n        }\r\n\r\n        if (achA) {\r\n            achA.forEach(item => {\r\n                item.classList.add(\"link-light\");\r\n                item.classList.remove(\"link-primary\");\r\n            });\r\n        }\r\n\r\n        if (main) {\r\n            main.classList.add(\"dark\");\r\n            main.classList.remove(\"light\");\r\n\r\n        }\r\n\r\n        if (prof) {\r\n            profileContainer.classList.add(\"dark-profile-cont\");\r\n            profileContainer.classList.remove(\"light-profile-cont\");\r\n        }\r\n\r\n        if (toggle) {\r\n            toggle.classList.add(\"link-light\");\r\n            toggle.classList.remove(\"link-primary\");\r\n        }\r\n\r\n        tables.forEach(table => {\r\n            table.classList.add(\"table-dark\")\r\n        });\r\n\r\n        localStorage.setItem('dark-mode', 'dark');\r\n    }\r\n});\r\n\r\nligbtn.addEventListener(\"click\", function (e) {\r\n    if (e.target.hidden === false) {\r\n        ligbtn.hidden = true\r\n        darkBtn.hidden = false\r\n        if (hcontainer) {\r\n            hcontainer.classList.toggle(\"dark-mode\");\r\n            hcontainer.classList.remove(\"hdark\");\r\n\r\n            for (const item of tableLinks) {\r\n                item.classList.remove(\"link-light\");\r\n                item.classList.add(\"link-primary\");\r\n            }\r\n\r\n        }\r\n\r\n        if (lab) {\r\n            lab.classList.add(\"light-lab-cont\");\r\n            lab.classList.remove(\"dark-lab-cont\");\r\n        }\r\n\r\n        if (about) {\r\n            about.classList.add(\"light-about-cont\");\r\n            about.classList.remove(\"dark-about-cont\");\r\n\r\n            aboutA.classList.remove(\"link-light\");\r\n            aboutA.classList.add(\"link-primary\");\r\n        }\r\n\r\n        if (tcontainer) {\r\n            tcontainer.classList.toggle(\"dark-mode\");\r\n        }\r\n\r\n        if (achA) {\r\n            achA.forEach(item => {\r\n                item.classList.remove(\"link-light\");\r\n                item.classList.add(\"link-primary\");\r\n            });\r\n        }\r\n\r\n        if (subh) {\r\n            subh.classList.add(\"light\");\r\n            subh.classList.remove(\"dark\");\r\n            embvid.classList.add(\"light\");\r\n            embvid.classList.remove(\"dark\");\r\n            textarea.classList.add(\"light\");\r\n            textarea.classList.remove(\"dark\");\r\n            bonusTxt.classList.add(\"light\");\r\n            bonusTxt.classList.remove(\"dark\");\r\n\r\n            bonusContainer.classList.add(\"light-bonus-cont\");\r\n            bonusContainer.classList.remove(\"dark-bonus-cont\");\r\n            counterCont.classList.add(\"light-counter-cont\");\r\n            counterCont.classList.remove(\"dark-counter-cont\");\r\n        }\r\n        if (main) {\r\n            main.classList.add(\"light\");\r\n            main.classList.remove(\"dark\");\r\n\r\n        }\r\n\r\n        if (prof) {\r\n            profileContainer.classList.add(\"light-profile-cont\");\r\n            profileContainer.classList.remove(\"dark-profile-cont\");\r\n        }\r\n\r\n        if (toggle) {\r\n            toggle.classList.add(\"link-primary\");\r\n            toggle.classList.remove(\"link-light\");\r\n        }\r\n\r\n        tables.forEach(table => {\r\n            table.classList.remove(\"table-dark\")\r\n        });\r\n\r\n        localStorage.setItem('dark-mode', 'light');\r\n    }\r\n});\r\n\n\n//# sourceURL=webpack://dictatube/./assets/scripts/base/toggle_mode.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./assets/scripts/base/index.js");
/******/ 	
/******/ })()
;