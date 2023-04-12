import CostTotals from './Reports/CostTotals.js'
import EntryPage from './EntryPage.js'
import LoginPage from './LoginPage.js'
import LandingPage from './LandingPage.js'
import MealsPage from './Meals/MealsPage.js'
import InventoryPage from './InventoryPage.js'
import HouseholdForm from './Households/HouseholdForm.js'
import HouseholdPage from './Households/HouseholdPage.js'
import HouseholdsReport from './Reports/HouseholdsReport.js'
import Ingredients from './Ingredients/IngredientList.js'
import IngredientPage from './Ingredients/IngredientPage.js'
import IngredientsReport from './Reports/IngredientsReport.js'
import IngPurchaseReport from './Reports/IngPurchaseReport.js'
import StationList from './Stations/StationList.js'
import ReportsPage from "./Reports/ReportsPage.js"
import UserPage from "./User/UserPage.js"
import UserList from "./User/UserList.js"
import NewUserPage from "./User/NewUserPage.js"
import MealPlan from './Meals/MealList.js'
import MealPlanReport from './Reports/MealPlanReport.js'
import MealHistoryReport from './Reports/MealHistoryReport.js'
import Packaging from './Packaging/PackagingList.js'
import PackagingPage from './Packaging/PackagingPage.js'
import PackagingReport from './Reports/PackagingReport.js'
import PackagingReturns from './Reports/PackagingReturns.js'
import PackagingPurchaseReport from './Reports/PackagingPurchaseReport.js'
import PwResetPage from './PwResetPage.js'
import Recipe from './Recipe/RecipeList.js'
import RecipePage from './Recipe/RecipePage.js'
import UnderConstruction from './components/UnderConstruction.js'
import Navbar from './Navbar.js'
import React from 'react'
import { useState } from 'react'
import { Box } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
// import { useOutsideClick} from './components/Dropdown'
import './App.css';

// SERVER IP 4.236.185.213

const style = {
    padding: '10px',
    // border: '1px solid black',
    display: 'flex',
    justifyContent: 'space-between',
};

const App = () => {
    const [loginState, setLoginState] = useState({
        username: "",
        isAuthenticated: false,
        isAdmin: false
    })

    // const handleClickOutside = () => {};
    // const ref = useOutsideClick(handleClickOutside);
    
    const handleHeaderClick = (event) => {
        event.stopPropagation();
      };

    /*const readLoginCookie = () => {
        const parseCookie = str =>
            str
            .split(';')
            .map(v => v.split('='))
            .reduce((acc, v) => {
            acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
            return acc;
        }, {});
        return parseCookie(document.cookie);
    }*/

    const handleLogout = () => {
        document.cookie = 'username=;'
        document.cookie = 'isAuthenticated=false;'
        document.cookie = 'isAdmin=false;'
        setLoginState({
            username: '',
            isAuthenticated: false,
            isAdmin: false
        })
    }

    const handlePageClick = (pageName) => {
        console.log(pageName)
        switch(pageName) {
            case 'cost-totals': setCurrPage(<CostTotals handlePageClick={handlePageClick} />); break;
            case 'loginPage': setCurrPage(<LoginPage loginState={loginState} setLoginState={setLoginState} handlePageClick={handlePageClick} />); break;
            case 'newUserPage': setCurrPage(<NewUserPage handlePageClick={handlePageClick} />); break;
            case 'pwResetPage': setCurrPage(<PwResetPage handlePageClick={handlePageClick} />); break;
            case 'landingPage': setCurrPage(<LandingPage handlePageClick={handlePageClick} />); break;
            case 'mealsPage': setCurrPage(<MealsPage handlePageClick={handlePageClick} />); break;
            case 'households': setCurrPage(<HouseholdPage handlePageClick={handlePageClick} />); break;
            case 'householdForm': setCurrPage(<HouseholdForm />); break;
            case 'households-report': setCurrPage(<HouseholdsReport handlePageClick={handlePageClick} />); break;
            case 'ingredients': setCurrPage(<Ingredients handlePageClick={handlePageClick} />); break;
            case 'ingredientPage': setCurrPage(<IngredientPage handlePageClick={handlePageClick} />); break;
            case 'ingredients-report': setCurrPage(<IngredientsReport handlePageClick={handlePageClick} />); break;
            case 'ing-purchase-report': setCurrPage(<IngPurchaseReport handlePageClick={handlePageClick} />); break;
            case 'inventoryPage': setCurrPage(<InventoryPage handlePageClick={handlePageClick} />); break;
            case 'packaging': setCurrPage(<Packaging handlePageClick={handlePageClick} />); break;
            case 'packagingPage': setCurrPage(<PackagingPage handlePageClick={handlePageClick} />); break;
            case 'packaging-report': setCurrPage(<PackagingReport handlePageClick={handlePageClick} />); break;
            case 'packaging-return-report': setCurrPage(<PackagingReturns handlePageClick={handlePageClick} />); break;
            case 'pack-purchase-report': setCurrPage(<PackagingPurchaseReport handlePageClick={handlePageClick} />); break;
            case 'stations': setCurrPage(<StationList handlePageClick={handlePageClick} />); break;
            case 'meals': setCurrPage(<MealPlan handlePageClick={handlePageClick} />); break;
            case 'meal-plan-report': setCurrPage(<MealPlanReport handlePageClick={handlePageClick} />); break;
            case 'meal-history-report': setCurrPage(<MealHistoryReport handlePageClick={handlePageClick} />); break;
            case 'recipes': setCurrPage(<Recipe handlePageClick={handlePageClick} />); break;
            case 'recipePage': setCurrPage(<RecipePage handlePageClick={handlePageClick} setCurrPage={setCurrPage} />); break;
            case 'reports': setCurrPage(<ReportsPage handlePageClick={handlePageClick} />); break;
            case 'userPage': setCurrPage(<UserPage handlePageClick={handlePageClick} />); break;
            case 'userList': setCurrPage(<UserList handlePageClick={handlePageClick} />); break;
            case 'entryPage': setCurrPage(<EntryPage handlePageClick={handlePageClick}/>); break;
            case 'under-construction': setCurrPage(<UnderConstruction handlePageClick={handlePageClick}/>); break;
            default: setCurrPage(<LandingPage handlePageClick={handlePageClick} />); break;
        }
    }

    const [currPage, setCurrPage] = useState(<EntryPage handlePageClick={handlePageClick} setLoginState={setLoginState} />);

    // useEffect(() => {setCurrPage(<EntryPage handlePageClick={handlePageClick}/>)}, [])
    // Charcoal: #898989
    // Ultraviolet: #5A5874

    const theme = createTheme({
        palette: {
            lightGreen: {
                main: '#9AB847', // light green logo color
                contrastText: '#fff'
            },
            darkGreen: {
                main: '#636182',
                contrastText: '#fff'
            },
            lightBlue: {
                main: '#636182',
                contrastText: '#fff'
            },
            lightOrange: {
                main: '#636182',
                contrastText: '#fff'
            },
            darkBlue: {
                // main: '#404851',
                main: '#636182',
                contrastText: '#fff'
            },
        }
    })

    return (
        <ThemeProvider theme={theme}>
        <div className="App" style={style} onClick={handleHeaderClick}>
            <Navbar handlePageClick={handlePageClick} handleLogout={handleLogout} loginState={loginState} />
            <Box sx={{
                bgcolor: (theme) => theme.palette.background.default,
                minHeight: "100%",
                width: '90%',
                margin: 'auto',
                marginTop: {lg: '5%', md: '6%', sm: '10%', xs: '12%'},
            }}>
                {currPage}
            </Box>
        </div>
        </ThemeProvider>
    );
};

export default App;
