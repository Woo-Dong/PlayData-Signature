import React from "react";
// reactstrap components
import {
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Container,
  UncontrolledTooltip
} from "reactstrap";

function IndexNavbar(props) {
  const [navbarColor, setNavbarColor] = React.useState("navbar-transparent");

	React.useEffect(() => {
		
		const updateNavbarColor = () => {
		if (
			document.documentElement.scrollTop > 399 ||
			document.body.scrollTop > 400
		) {
			setNavbarColor("");
		} else if (
			document.documentElement.scrollTop < 399 ||
			document.body.scrollTop < 400
		) {
			setNavbarColor("navbar-transparent");
		}
		};
		window.addEventListener("scroll", updateNavbarColor);
		return function cleanup() {
		window.removeEventListener("scroll", updateNavbarColor);
		};
	});

	return (
		<div>
			<Navbar className={"fixed-top " + navbarColor} expand="md" color="primary">
				<Container>
					<div className="navbar-translate">
						<NavbarBrand
							href="/"
							id="navbar-brand"
						>
							Signature
						</NavbarBrand>
						<UncontrolledTooltip target="#navbar-brand">
							(시그니처)
						</UncontrolledTooltip>
					</div>

					<div className="col-md-auto">
						<Nav navbar className="nav-open">
						<NavItem>
							<NavLink
								onClick={props.toIndexHeader}
								variant="primary"
							>
								<i className="now-ui-icons shopping_shop"></i>
								<p>Home</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toMainBoard}
								variant="primary"
							>
								<i className="now-ui-icons loader_gear"></i>
								<p>Dash Board</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toGraphSection}
							>
								<i className="now-ui-icons loader_gear"></i>
								<p>graph</p>
							</NavLink>
						</NavItem>
					</Nav>
					</div>

					<div className="col-md-auto"></div>
				</Container>
			</Navbar>
		</div>
		);
	}

export default IndexNavbar;