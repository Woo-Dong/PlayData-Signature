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
							(Signature Project)
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
								onClick={props.toDomesticSection}
								variant="primary"
							>
								<i className="now-ui-icons design_bullet-list-67"></i>
								<p>국내-일별</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toGlobalSection}
							>
								<i className="now-ui-icons media-2_sound-wave"></i>
								<p>셰게 상황</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toPredGraphSection}
							>
								<i className="now-ui-icons media-2_sound-wave"></i>
								<p>predict</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toNewsSection}
							>
								<i className="now-ui-icons education_paper"></i>
								<p>news</p>
							</NavLink>
						</NavItem>

						<NavItem>
							<NavLink
								onClick={props.toInfoSection}
							>
								<i className="now-ui-icons business_badge"></i>
								<p>info</p>
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