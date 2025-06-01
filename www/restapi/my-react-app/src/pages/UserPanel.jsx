import "./UserPanel.css"
import "./Buttons.css"
import {useNavigate} from "react-router-dom";

function UserPanel () {

    const navigate = useNavigate();

    return (
        <div className="container">
            <div className="btn-group">
                <button className="btn btn-transparent" onClick={() => navigate('/user/me')}>
                    My profile
                </button>
                <button className="btn btn-yellow">
                    Log out
                </button>
            </div>
        </div>
    );
}
export default UserPanel;