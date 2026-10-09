function f = mh_sir_rhs(beta, gamma, N)
%MH_SIR_RHS  Ve phai SIR dang chuan: y = [S; I; R] (VECTO COT),
%   S' = -beta S I/N,  I' = beta S I/N - gamma I,  R' = gamma I.
f = @(t, y) [ -beta * y(1) * y(2) / N;
               beta * y(1) * y(2) / N - gamma * y(2);
               gamma * y(2) ];
end
