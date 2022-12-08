import React from 'react'

// Packaging Row component
// Takes: key of current row, the state of the Packaging Page's Packaging list, deletePackaging callback, handleEditClick callback
// Returns a Packaging table row component 
const PackagingRow = (props) => {
    const {thisKey, package_item, deletePackaging, handleEditClick } = props;
    const key = thisKey;
    const pac = package_item;

    // HTML structure of this component
    return (
        <tr key={key}>
            <td>{pac.p_id}</td>
            <td>{pac.package_type}</td>
            <td>{pac.unit_qty}</td>
            <td>{pac.unit_cost}</td>
            <td>{pac.qty_holds}</td>
            <td>{pac.unit}</td>
            <td>{pac.returnable}</td>
            <td>{String(pac.in_date)}</td>
            <td>{pac.in_qty}</td>
            <td>{String(pac.exp_date)}</td>
            <td>{pac.qty_on_hand}</td>
            <td>{pac.flat_fee}</td>
            <td>{pac.psupplier_name}</td>
            <td>{pac.pref_psupplier_name}</td>
            {/* When edit is clicked, handleEditClick is called with this row's key */}
            <td><button onClick={() => handleEditClick(key)}>Edit</button></td>
            {/* When delete is clicked, deletePackaging is called with this row's key */}
            <td><button onClick={() => deletePackaging(key)}>Delete</button></td>
        </tr>
    )
}

export default PackagingRow;