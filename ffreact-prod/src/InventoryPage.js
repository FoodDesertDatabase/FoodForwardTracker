import React from 'react'
import { useState } from 'react'
import { Fragment } from 'react'
import { Container, Button, Typography } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Packaging from './Packaging/PackagingList.js'
import PackagingPage from './Packaging/PackagingPage.js'

import Ingredients from './Ingredients/IngredientList.js'
import Dropdown from './components/Dropdown'
import { CssBaseline, Box } from '@mui/material'

const style = {
    padding: '10px',
    border: '1px solid black',
    display: 'flex-box',
    justifyContent: 'space-between',
};

const theme = createTheme({
    palette: {
        lightGreen: {
            main: '#9AB847', // light green logo color
            contrastText: '#fff'
        },
        darkGreen: {
            main: '#093B31',
            contrastText: '#fff'
        },
        lightBlue: {
            main: '#3E8477',
            contrastText: '#fff'
        },
        lightOrange: {
            main: '#A35426',
            contrastText: '#fff'
        },
        darkBlue: {
            main: '#070D3A',
            contrastText: '#fff'
        }
    }
})

const LandingPage = (props) => {
    const [currPage, setCurrPage] = useState();
    const handlePageClick = (pageName) => {
        console.log(pageName)
        switch(pageName) {
            case 'ingredients': setCurrPage(<Ingredients handlePageClick={handlePageClick} />); break;
            case 'packaging': setCurrPage(<Packaging handlePageClick={handlePageClick} />); break;
            case 'packagingPage': setCurrPage(<PackagingPage></PackagingPage>); break;

        }
    } 
    return (
        <ThemeProvider theme={theme}>
        <div style={style}>
        <CssBaseline />
        <Dropdown
            trigger={<Button color='lightGreen' variant='contained'>Inventory Page</Button>}
            menu={[
                <button color='lightGreen' ref={props.ref} type="button" onClick={() => handlePageClick('ingredients')}>
                    Ingredients</button>,
                <button color='lightGreen' ref={props.ref} type="button" onClick={() => handlePageClick('packagingPage')}>
                    Packaging</button>,
                ]}/>
            {currPage}
        </div>
        </ThemeProvider>
    );   
}

export default LandingPage;