import React, {Fragment, useState} from 'react'
import axios from 'axios'
import RecipeForm from './RecipeForm.js'
import EditableRecipeRow from './EditableRecipeRow.js'
import RecipeRow from './RecipeRow.js'
import Error from '../Error.js'
import DisplayMessage from '../DisplayMessage.js'
import './RecipeList.css'


// Recipe List Component
export default function RecipeList() {

    const [recipeID, setRecipe] = useState();
    const [editRecipeID, setEditRecipeID] = useState(null);
    const [editFormData, setEditFormData] = useState(null);
    const [errorComponent, setErrorComponent] = useState(null);
    const [displayMsgComponent, setdisplayMsgComponent] = useState(null);

    const getDBRecipe = () => {
        axios({
            method: "GET",
            url:"/recipe/"
          }).then((response)=>{
            const recipeData = response.data
            setRecipe(recipeData);
          }).catch((error) => {
            if (error.response) {
              console.log(error.response);
              console.log(error.response.status);
              console.log(error.response.headers);
              }
          });
    }

    const postDBRecipe = () => {
        axios({
            method: "POST",
            url:"/recipe/",
            data: recipeID
          }).then((response)=>{
            getDBRecipe();
          }).catch((error) => {
            if (error.response) {
              console.log(error.response);
              console.log(error.response.status);
              console.log(error.response.headers);
              }
          });
        setdisplayMsgComponent(<DisplayMessage msg='Submitting changes to database!'/>);
    }

    const handleError = (errCode) => {
        if (errCode === 'DuplicateKey') {
            setErrorComponent(
                <Error text="Ingredient ID already found!"/>
            )
        }
    }
    const clearError = () => {
        setErrorComponent(null);
    }

    const addRecipe = (recipe) => {
        const lastID = recipe[recipe.length - 1]['r_name'];
        recipe['r_name'] = lastID + 1;
        let newRecipe = [...recipe, recipe];
        setRecipe(newRecipe);
        clearError();
        // Check to see if we already have a duplicate Ingredient Name
        // if (!ingredients.find((ing) => ing.i_id === ing.i_id))
        // {
        //     let newIngredients = [...ingredients, ingredient];
        //     setIngredients(newIngredients);
        //     clearError();
        // }
        // else {
        //     // If this ingredient is already in ingredients list, display error message
        //     handleError('DuplicateKey');
        // }
    }

    const deleteRecipe = (key) => {
        const recipeID = key; 
        let newRecipe = [...recipeID];
        newRecipe.splice(recipeID, 1);
        setRecipe(newRecipe);
    }

    const updateRecipe = (key) => {
        let thisID = recipeID[key]['i_id'];
        if (recipeID.find((recipes) => recipes.r_num === thisID))
        {
            let newRecipe = [...recipeID];
            newRecipe[key] = editFormData;
            setEditRecipeID(null);
            setRecipe(newRecipe)
            clearError();
        }
        else {
            // If this Ingredient is already in ingredients list, display error message
            handleError('DuplicateKey');
        }
        
    }

    const handleEditFormChange = (event) => {
        // Get the name and value of the changed field
        const fieldName = event.target.getAttribute('name');
        const fieldValue = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
        // Create new Ingredient object before setting state
        const newEditFormData = {...editFormData};
        newEditFormData[fieldName] = fieldValue;
        // Set state with new ingredient object
        setEditFormData(newEditFormData);
    }
    const updateEditForm = (names, values) => {
        const newEditFormData = {...editFormData};
        for (let i = 0; i < names.length; i++) {
          newEditFormData[names[i]] = values[i];
          console.log('(' + names[i] + ', ' + values[i] + ')', newEditFormData.aFlag);
        }
        setEditFormData(newEditFormData);
      }

    const handleEditClick = (key) => {
        setEditRecipeID(key);
        setEditFormData(recipeID[key]);
    }
    const handleCancelClick = () => {
        setEditRecipeID(null);
        setEditFormData(null);
    }

    // The HTML structure of this component
    return (
        /* Fragment is an invisible tag that can be used to encapsulate multiple JSX elements without changing the HTML structure of the page */
        <div class='table-div'>
            <table className='main-table'>
                <thead>
                    <h3>Recipes</h3>
                    <tr>
                        <th>Recipe Number</th>
                        <th>Recipe Name</th>
                        <th>Recipe ID</th>
                        <th>Amount</th>
                        <th>Unit</th>
                        <th>Recipe Ingredient</th>
                        <th>Recipe Ingredient Recipe Number</th>
                        <th>Recipe Instruction ID</th>
                        <th>Step number</th>
                        <th>Step Instruction</th>
                        <th>Station Name</th>
                        <th>Recipe Instruction Number</th>
                    </tr>
                </thead>
                <tbody>
                    {/* Show a row for each ingredient in ingredients.*/}
                    {recipeID.map((recipe, key) => {
                        const thisKey = key;
                        return(
                            <Fragment>
                                {
                                // If this ingredient is the one to be edited, show an editable row instead
                                editRecipeID === thisKey 
                                ? <EditableRecipeRow thisKey={thisKey} editFormData={editFormData} updateRecipe={updateRecipe} handleEditFormChange={handleEditFormChange} updateEditForm={updateEditForm} handleCancelClick={handleCancelClick}/>
                                : <RecipeRow thisKey={thisKey} recipe={recipe} deleteRecipe={deleteRecipe} handleEditClick={handleEditClick}/>
                                }
                            </Fragment>
                        );
                    })}
                </tbody>
            </table>
            <h3>Add Recipe</h3>
            <RecipeForm addRecipe={addRecipe}></RecipeForm>
            <button onClick={postDBRecipe}>Submit Changes</button>
            {errorComponent}
            {displayMsgComponent}
        </div>
    )
}
